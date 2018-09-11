
def flatten_dict(tree, parent_key='', sep=' '):
    """
    Recursively flatten a nested dictionary into a single level whose keys are
    phrases.

    For example, given the following dict:

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

    The separator can be configured as an arbitrary string.
    """
    flattened = []
    for key, value in tree.items():
        new_key = sep.join([parent_key, key]) if parent_key else key
        try:
            flattened.extend(flatten_dict(value, parent_key=new_key, sep=sep).items())
        except:
            flattened.append((new_key, value))

    return dict(flattened)
