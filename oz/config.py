"""
Makes module configuration variables accessible from multiple sources.
"""
import os
from collections import namedtuple
import configparser
from .util import flatten_dict

ConfigItem = namedtuple('ConfigItem', ['env_key', 'file_key', 'default'])

class Config(object):
    def __init__(self):
        self.items = {}
        self.from_file = {}

    def load(self, fname, overwrite=False):
        _, ext = os.path.splitext(fname)

        if ext.lower() == 'yml' or ext.lower() == 'yaml':
            parsed = flatten_dict(yaml.safe_load(open(fname)))
        else:
            parsed = ConfigParser()
            parsed.read(fname)

        if overwrite:
            self.from_file = parsed
        else:
            self.from_file.extend(parsed)

    def register(self, key, env_key=None, file_key=None, default=None):
        item = ConfigItem(env_key, file_key, default)
        self.items[key] = item

    def __getitem__(self, key):
        entry = self.items[key]
        val = None
        if entry.env_key:
            val = os.getenv(entry.env_key)

        if not val and entry.file_key:
            val = self.from_file.get(entry.file_key)

        if not val:
            val = entry.default

        return val

config = Config()
