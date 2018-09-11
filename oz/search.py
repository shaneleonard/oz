
import os
import logging
from itertools import combinations
import whoosh
import whoosh.fields
import whoosh.index
import whoosh.qparser

from .config import config
from .env import env

log = logging.getLogger(__name__)

config.register('search_index_path', default='.oz/index')

def create_search_index():
    """
    Set up a Whoosh search index based on the keys in the given spellbook.
    """
    # Try to open the index if it already exists and is recent.
    if os.path.exists(config['search_index_path']):
        idx_modified = os.path.getmtime(config['search_index_path'])
        spellbook_modified = os.path.getmtime(env['spellbook_path'])

        if spellbook_modified < idx_modified:
            return whoosh.index.open_dir(config['search_index_path'])
    else:
        os.makedirs(config['search_index_path'])

    schema = whoosh.fields.Schema(
                name=whoosh.fields.NGRAMWORDS(stored=True),
                contents=whoosh.fields.STORED)

    index = whoosh.index.create_in(config['search_index_path'], schema)
    writer = index.writer()

    for spell_name, spell_contents in env['flat_spellbook'].items():
        writer.add_document(name=spell_name, contents=spell_contents)

    writer.commit()

    return index

def find_spell(spell_symbol, context_hints, searcher):
    """
    Find the spell name in the spellbook which most likely corresponds to the
    spell symbol (eg a template variable from a parent spell).
    """
    qparser = whoosh.qparser.QueryParser('name', env['search_index'].schema)

    log.info("Searching {} with context {}".format(spell_symbol, context_hints))

    for n_query_terms in range(len(context_hints), -1, -1):
        for context in combinations(context_hints, n_query_terms):
            query_terms = ' '.join(list(context) + [spell_symbol])
            query = qparser.parse(query_terms)
            results = searcher.search(query)

            if len(results) == 1:
                log.info("Found {} from query {}".format(results[0]['name'],
                    query_terms))
                return results[0]

    return None

env.register('search_index', create_search_index)
