from __future__ import unicode_literals, division, absolute_import

import ftplib
import logging
import re

from flexget import plugin
from flexget.config_schema import one_or_more
from flexget.entry import Entry
from flexget.event import event
from flexget.plugin import DependencyError, PluginError

try:
    from ftputil.error import FTPOSError
    import ftputil
    import ftputil.session

    imported = True
except ImportError:
    imported = False

log = logging.getLogger('ftp_list')


class FTPList(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.host = None
        self.port = None
        self.FTP = None

    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'host': {'type': 'string'},
            'port': {'type': 'integer'},
            'ssl': {'type': 'boolean'},
            'dirs': one_or_more({'type': 'string'}),
            'recursion': {'type': 'boolean'},
            'recursion_depth': {'type': 'integer'},
            'retrieve': one_or_more({'type': 'string', 'enum': ['files', 'dirs', 'symlinks']}, unique_items=True)
        },
        'required': ['username', 'host']
    }

    @staticmethod
    def prepare_config(config):
        config.setdefault('retrieve', ['files'])
        config.setdefault('ssl', False)
        config.setdefault('dirs', [''])
        config.setdefault('port', 21)
        config.setdefault('recursion', False)
        if not isinstance(config['dirs'], list):
            config['dirs'] = [config['dirs']]
        if not isinstance(config['retrieve'], list):
            config['retrieve'] = [config['retrieve']]
        return config

    def _to_entry(self, path):
        entry = Entry()

        title = self.FTP.path.basename(path)
        location = self.FTP.path.abspath(path)

        entry['title'] = title
        entry['location'] = location
        entry['url'] = 'ftp://{}:{}@{}:{}/{}'.format(self.username, self.password, self.host, self.port, location)
        entry['filename'] = title

        log.debug('adding entry %s', entry)
        if entry.isvalid():
            return entry
        else:
            log.warning('tried to return an illegal entry: %s', entry)

    def on_task_input(self, task, config):
        if not imported:
            raise DependencyError('ftp_list', 'ftp_list', 'ftputil is required for this plugin')
        config = self.prepare_config(config)

        self.username = config.get('username')
        self.password = config.get('password')
        self.host = config.get('host')
        self.port = config.get('port')

        directories = config.get('dirs')
        recursion = config.get('recursion')
        recursion_depth = -1 if recursion else 0

        base_class = ftplib.FTP_TLS if config.get('ssl') else ftplib.FTP
        session_factory = ftputil.session.session_factory(port=self.port, base_class=base_class)
        try:
            log.verbose(
                'trying to establish connection to FTP: %s:<HIDDEN>@%s:%s', self.username, self.host, self.port)
            self.FTP = ftputil.FTPHost(self.host, self.username, self.password, session_factory=session_factory)
        except FTPOSError as e:
            raise PluginError('Could not connect to FTP: {}'.format(e.args[0]))

        entries = []
        for dir in directories:
            with self.FTP as ftp:
                if not ftp.path.isdir(dir):
                    log.warning('Directory %s is not a valid dir, skipping', dir)
                    continue
                for base, dirs, files in ftp.walk(dir):
                    current_depth = base.count('/')
                    if current_depth > recursion_depth != -1:
                        log.debug('recursion depth limit of %s reached, continuing', current_depth)
                        continue
                    if 'files' in config['retrieve'] or 'symlinks' in config['retrieve']:
                        for _file in files:
                            path = ftp.path.join(base, _file)
                            if ftp.path.isfile(path) and 'files' in config['retrieve'] or ftp.path.islink(
                                    path) and 'symlinks' in config['retrieve']:
                                log.debug('type match successful for file %s, trying to create entry', _file)
                                entries.append(self._to_entry(path))
                    if 'dirs' in config['retrieve'] or 'symlinks' in config['retrieve']:
                        for _dir in dirs:
                            path = ftp.path.join(base, _dir)
                            if ftp.path.isdir(path) and 'dirs' in config['retrieve'] or ftp.path.islink(
                                    path) and 'symlinks' in config['retrieve']:
                                log.debug('type match successful for directory %s, trying to create entry', _dir)
                                entries.append(self._to_entry(path))

        return entries


@event('plugin.register')
def register_plugin():
    plugin.register(FTPList, 'ftp_list', api_ver=2)
