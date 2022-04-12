# Copyright (C) 2017-2022 Aleksandr Popov
# Copyright (C) 2021-2022 Kirill Butin

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

"""This module implements the base classes for Activities."""

import logging
from dsplab.helpers import import_entity

LOG = logging.getLogger(__name__)


class ActivityMeta(type):
    """Metaclass for Activity."""

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        cls._class_info = {}

        try:
            cls._class_info['doc'] = attrs['__doc__']
        except KeyError:
            cls._class_info['doc'] = ''

        cls._class_info['class'] = name

    def class_info(cls):
        """Return the information about activity.

        Returns
        -------
        : dict
            Information about class of activity.
        """
        return cls._class_info

    def __call__(cls, *args, **kwargs):
        res = type.__call__(cls, *args, **kwargs)
        setattr(res, 'class_info', cls.class_info)

        return res


class Activity(metaclass=ActivityMeta):
    # pylint: disable=too-few-public-methods
    """Any activity is the something that may be called and can provide the
    information about itself.

    To get working activity the __call__ method must be implemented.
    """

    def __call__(self, *args, **kwargs):
        """Call activity."""
        raise NotImplementedError


class Work(Activity):
    """Work is data processing that can be done in a variety of ways."""

    def __init__(self, descr=None, worker=None):
        super().__init__()
        self.set_descr(descr)
        self.set_worker(worker)

    def set_descr(self, descr):
        """Set description."""
        self._descr = descr

    def get_descr(self):
        """Return description."""
        return self._descr

    descr = property(get_descr, set_descr, doc='Description of work')

    def set_worker(self, act):
        """Set worker for doing work.

        Worker must be callable.
        """
        self._worker = act

    def __call__(self, *args, **kwargs):
        """Do work."""
        return self._worker(*args, **kwargs)


def get_work_from_dict(work_dict, params=None):
    """Create and return Work instance described in dictionary."""

    if 'worker' not in work_dict:
        raise RuntimeError('No worker in work_dict')

    return Work(_get_descr(work_dict),
                _get_worker(work_dict['worker'], params))


def _get_descr(work_dict):
    try:
        return work_dict['descr']
    except KeyError:
        return ''


def _get_worker(worker_dict, params):
    wr_type = _get_worker_type(worker_dict)

    call_name = worker_dict[wr_type]

    if 'params' in worker_dict:
        return _worker_with_params(worker_dict, call_name, params)

    return _worker_no_params(call_name, wr_type)


def _get_worker_type(worker_dict):
    if 'class' in worker_dict:
        return 'class'

    if 'function' in worker_dict:
        return 'function'

    raise RuntimeError('Work must be \'class\' or \'function\'')


def _worker_with_params(worker_dict, call_name, params):
    wr_pars = worker_dict['params'].copy()

    for key in wr_pars:
        if not isinstance(wr_pars[key], str):
            continue

        if not wr_pars[key]:
            continue

        if wr_pars[key][0] != '$':
            continue

        wr_pars[key] = params[wr_pars[key][1:]]

    return import_entity(call_name)(**wr_pars)


def _worker_no_params(call_name, worker_type):
    if worker_type == 'class':
        return import_entity(call_name)()

    return import_entity(call_name)
