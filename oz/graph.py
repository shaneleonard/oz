
import logging
from jinja2 import meta, Environment
import networkx as nx
from .env import env
from .search import find_spell

log = logging.getLogger(__name__)
env.register('jinja', Environment)

def child_spells(spell):
    """
    Parses a (Jinja template) spell to determine what variables are required as
    template inputs. These variables are referred to as 'spell symbols'.
    """
    parsed = env['jinja'].parse(spell)
    found = meta.find_undeclared_variables(parsed)
    if found:
        log.info("Found children {}".format(found))
    return found

def build_dependency_graph(spell_type, context, searcher, dag=None):
    if dag is None:
        dag = nx.DiGraph()

    spell = find_spell(spell_type, context, searcher)
    dag.add_node(spell_type, spell=spell)

    for child in child_spells(spell['contents']):
        build_dependency_graph(child, context, searcher, dag)
        dag.add_edge(child, spell_type)
        if not nx.is_directed_acyclic_graph(dag):
            raise NotImplementedError

    return dag
