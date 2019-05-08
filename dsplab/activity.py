# Copyright (C) 2017-2019 Aleksandr Popov

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

""" This module implements the base classes for Activities. """

import logging
from warnings import warn
from dsplab.helpers import import_entity

LOG = logging.getLogger(__name__)


class ActivityMeta(type):
    """ Metaclass for Activity. """
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._class_info = {}
        try:
            cls._class_info['descr'] = attrs['__doc__']
        except KeyError:
            cls._class_info['descr'] = ""
        cls._class_info['class'] = name

    def class_info(cls):
        """ Return the information about activity.

        Returns
        -------
        : dict
            Information about class of activity.
        """
        return cls._class_info

    def __call__(cls, *args, **kwargs):
        res = type.__call__(cls, *args, **kwargs)
        setattr(res, "class_info", cls.class_info)
        return res


class Activity(metaclass=ActivityMeta):
    """ Any activity -- something that may be called and can provide
    the information about itself. To get working activity the __call__
    method must be implemented. """
    def __init__(self):
        self._info = self._class_info.copy()

    def set_descr(self, descr):
        """ Set description of activity. """
        self._info['descr'] = descr

    def info(self, as_string=None):
        """ Return the information about activity.

        Returns
        -------
        : dict
            Information about activity.

        """
        if as_string is not None:
            warn("as_string is deprecated and ignored")
        return self._info


class Worker(Activity):
    """ Worker is activity for doing some work. """
    def __init__(self):
        super().__init__()
        self._params = []

    def add_param(self, name, value=None):
        """ Add parameter and make record about it in info. """
        warn("Worker.add_param() is deprecated. Use _reg_param() instead.")
        setattr(self, name, value)
        self._reg_param(name)

    def _reg_param(self, name):
        """Add parameter to the list of parameters whose values should
        be included in the info."""
        if name in self._params:
            return
        self._params.append(name)

    def info(self, as_string=None):
        """Return actual info about worker including parameters
        values."""
        res = self._info.copy()

        if not self._params:
            return res

        res['params'] = {}
        for key in self._params:
            value = getattr(self, key)
            res['params'][key] = value

        if as_string is not None:
            warn("as_string is deprecated and ignored")

        return res


class Work(Activity):
    """ Work is activity which has some worker. Different workers can
    be used for doing the same work. """
    def __init__(self, descr="", worker=None):
        super().__init__()
        self.set_descr(descr)
        self.set_worker(worker)

    def set_worker(self, worker):
        """ Set worker for doing work. """
        self.worker = worker
        self._info['worker'] = None
        try:
            self._info['worker'] = worker.info()
        except (KeyError, AttributeError):
            pass

    def __call__(self, *args, **kwargs):
        """ Do work. """
        res = self.worker(*args, **kwargs)
        return res


def get_work_from_dict(settings, params=None):
    """Create and return Work instance described in dictionary."""
    if 'descr' in settings:
        descr = settings['descr']
    else:
        descr = ""

    if 'worker' not in settings:
        raise RuntimeError("No worker in settings")
    worker_settings = settings['worker']

    if 'class' in worker_settings.keys():
        key = 'class'
    elif 'function' in worker_settings.keys():
        key = 'function'
    else:
        raise RuntimeError("Work must be 'class' or 'function'")

    worker_name = worker_settings[key]

    if 'params' in worker_settings.keys():
        worker_params = worker_settings['params']

        for key in worker_params:
            if isinstance(worker_params[key], str):
                if worker_params[key]:
                    if worker_params[key][0] == "$":
                        params_key = worker_params[key][1:]
                        try:
                            worker_params[key] = params[params_key]
                        except KeyError:
                            msg = "${} not found in params".format(params_key)
                            raise RuntimeError(msg)

        worker = import_entity(worker_name)(**worker_params)
    else:
        if key == 'class':
            worker = import_entity(worker_name)()
        else:
            worker = import_entity(worker_name)

    work = Work(descr, worker)
    return work
