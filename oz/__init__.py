# -*- coding: utf-8 -*-

"""Top-level package for Oz the Powerful."""

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = """Shane William Leonard"""
__email__ = 'shane.william.leonard@gmail.com'
__version__ = '0.3.0'

from . import env
from . import config
from . import cli
from . import search
from . import graph
from . import spellbook
from . import util
