"""Helpers."""

import importlib
import json


def is_iterable(obj):
    """Check if obj is iterable."""

    try:
        iter(obj)
    except TypeError:
        return False

    return True


def import_entity(name):
    """Import class by name."""

    parts = name.split('.')
    entity_name = parts[-1]

    module_name = '.'.join(parts[:-1])
    if module_name == '':
        module_name = '__main__'

    module = importlib.import_module(module_name)
    entity = getattr(module, entity_name)

    return entity


def pretty_json(some_object):
    """Return json representation of object."""
    return json.dumps(some_object,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))
