# -*- coding: utf-8 -*-

"""Console script for oz_cli."""
import sys
import os
from itertools import combinations
import click
import yaml
import whoosh
import whoosh.fields
import whoosh.index
import whoosh.qparser
from jinja2 import Environment, meta

JINJA_ENV = Environment()
"""
Default environment for parsing Jinja2 templates.
"""

SEARCH_IDX = None
"""
Whoosh search index of spellbook contents.
"""

def get_spellbook_file_name():
    spellbook_fname = './.oz.yaml'
    while (not os.path.isfile(spellbook_fname) and
           os.path.exists(os.path.dirname(spellbook_fname))):
        spellbook_fname = os.path.join(spellbook_fname)

    if not os.path.isfile(spellbook_fname):
        return None

    return spellbook_fname

def load_spellbook():
    spellbook_fname = get_spellbook_file_name()
    if spellbook_fname is None:
        return None

    with open(spellbook_fname) as spellbook_file:
        spellbook = yaml.safe_load(spellbook_file)

    return spellbook

def flatten_spellbook(spellbook, parent_key=''):
    """
    Recursively flatten a nested dictionary into a single level whose keys are
    phrases.

    For example, given the following spellbook:

    ..code-block:: python

        {
            'my': {
                'git': {
                    'branch': 'master'
                }
            },
            'flash script': {
                'start address': 0x400000,
                'unflashed bytes': 0xff
            },
            'test': 'tox'
        }

    The flattened version is:

    ..code-block:: python

        {
            'my git branch': 'master',
            'flash script start address': 0x400000,
            'flash script unflashed bytes': 0xff,
            'test': 'tox'
        }
    """
    spells = []
    for key, value in spellbook.items():
        new_key = ' '.join([parent_key, key]) if parent_key else key
        try:
            spells.extend(flatten_spellbook(value, parent_key=new_key).items())
        except:
            spells.append((new_key, value))

    return dict(spells)

def index_spellbook(spellbook):
    """
    Set up a Whoosh search index based on the keys in the given spellbook.
    """
    global SEARCH_IDX
    schema = whoosh.fields.Schema(
                spell_name=whoosh.fields.NGRAMWORDS(stored=True),
                spell_contents=whoosh.fields.STORED)
    if not os.path.exists('.whoosh_index'):
        os.mkdir('.whoosh_index')
    SEARCH_IDX = whoosh.index.create_in('.whoosh_index', schema)
    writer = SEARCH_IDX.writer()

    for spell_name, spell_contents in spellbook.items():
        writer.add_document(spell_name=spell_name, spell_contents=spell_contents)

    writer.commit()

def spell_dependencies(spell):
    """
    Parses a (Jinja template) spell to determine what variables are required as
    template inputs. These variables are referred to as 'spell symbols'.
    """
    parsed = JINJA_ENV.parse(spell)
    return meta.find_undeclared_variables(parsed)

def resolve_spell_dependency(spell_symbol, context_hints):
    """
    Find the spell name in the spellbook which most likely corresponds to the
    spell symbol (eg a template variable from a parent spell).
    """
    qparser = whoosh.qparser.QueryParser('spell_name', SEARCH_IDX.schema)
    with SEARCH_IDX.searcher() as searcher:
        for n_query_terms in range(len(context_hints), 0, -1):
            for context in combinations(context_hints, n_query_terms):
                query_terms = ' '.join(list(context) + [spell_symbol])
                query = qparser.parse(query_terms)
                results = searcher.search(query)
                if len(results) > 0:
                    print(query_terms)
                    print(len(results))
                    print(results[0])

def search_spellbook_index(query_terms):
    qparser = whoosh.qparser.QueryParser('spell_name', SEARCH_IDX.schema)
    with SEARCH_IDX.searcher() as searcher:
        query = qparser.parse(query_terms)
        results = searcher.search(query)
        for result in results:
            print(result['spell_name'])

@click.command()
@click.argument('args', nargs=-1)
def main(args=None):
    """Console script for oz."""
    raw_spellbook = load_spellbook()
    if raw_spellbook is None:
        print("No spellbook found! Aborting.")
        return 1

    spellbook = flatten_spellbook(raw_spellbook)
    index_spellbook(spellbook)

    search_spellbook_index(' '.join(args))
    resolve_spell_dependency('branch', args)



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
