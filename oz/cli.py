# -*- coding: utf-8 -*-

"""Console script for oz_cli."""
import sys
import os
import logging
import click
import networkx as nx

from .env import env
from .config import config
from .graph import build_dependency_graph

config.register('logging_config_path',
                env_key='LOG_CFG',
                default='logging.yaml')
log = logging.getLogger()

def setup_logging():
    path = config['logging_config_path']
    if os.path.exists(path):
        with open(path, 'rt') as f:
            logging_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logging_config)
    else:
        logging.basicConfig(level=logging.INFO)

def evaluate(dag):
    for node in nx.topological_sort(dag):
        name = dag.nodes[node]['spell']['name']
        contents = dag.nodes[node]['spell']['contents']
        log.info("{} -> {}: {}".format(node, name, contents))

@click.command()
@click.argument('command', nargs=1)
@click.argument('context', nargs=-1)
def main(command, context):
    """Console script for oz."""
    setup_logging()

    with env['search_index'].searcher() as searcher:
        dag = build_dependency_graph(command, context, searcher)
        evaluate(dag)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
