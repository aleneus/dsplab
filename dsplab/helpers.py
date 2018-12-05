# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Helpers. """

import importlib
import json


def is_iterable(x):
    """ Check if x is iterable. """
    try:
        [e for e in x]
    except TypeError:
        return False
    return True


def import_entity(name):
    """ Import class by name. """
    parts = name.split('.')
    module_name = '.'.join(parts[:-1])
    entity_name = parts[-1]
    if len(module_name) == 0:
        module_name = '__main__'
    module = importlib.import_module(module_name)
    entity = getattr(module, entity_name)
    return entity


def pretty_json(some_object):
    """Return json representation of object."""
    return json.dumps(some_object, sort_keys=True, indent=4,
                      separators=(',', ': '))
