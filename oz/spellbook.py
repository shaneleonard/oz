import os
import logging
import yaml
from .util import flatten_dict
from .env import env
from .config import config

config.register('spellbook_name', default='.oz.yaml')

log = logging.getLogger(__name__)

def get_spellbook_file_name():
    spellbook_fname = config['spellbook_name']
    while (not os.path.isfile(spellbook_fname) and
           os.path.exists(os.path.dirname(spellbook_fname))):
        spellbook_fname = os.path.join(spellbook_fname)

    if not os.path.isfile(spellbook_fname):
        return None

    return spellbook_fname

def load_spellbook():
    spellbook_fname = env['spellbook_name']
    if spellbook_fname is None:
        return None

    with open(spellbook_fname) as spellbook_file:
        spellbook = yaml.safe_load(spellbook_file)

    return spellbook

env.register('spellbook_path', get_spellbook_file_name)
env.register('spellbook', load_spellbook)
env.register('flat_spellbook', lambda _: flatten_dict(env['spellbook']))
