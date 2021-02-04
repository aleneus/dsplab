# Copyright (C) 2017-2021 Aleksandr Popov
# Copyright (C) 2021 Kirill Butin

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
from warnings import warn
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
            cls._class_info['doc'] = ""
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
        setattr(res, "class_info", cls.class_info)
        return res


class Activity(metaclass=ActivityMeta):
    """Any activity is the something that may be called and can
    provide the information about itself. To get working activity the
    __call__ method must be implemented."""
    def __call__(self, *args, **kwargs):
        """Call activity."""
        raise NotImplementedError

    def set_descr(self, descr):
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        """Deprecated."""
        warn("Activity.set_descr() is deprecated. Use it for works only.")

    def info(self, as_string=None):
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        """Deprecated."""
        warn("info() is deprecated and returns stub, don't use it")
        return self.__class__.__name__


class Worker(Activity):
    """Deprecated."""
    def __init__(self):
        super().__init__()
        warn("Worker is deprecated. Use Activity instead.")

    def __call__(self, *args, **kwargs):
        """Call activity."""
        raise NotImplementedError

    def add_param(self, name, value=None):
        # pylint: disable=unused-argument
        """Deprecated."""
        warn("Worker.add_param() is deprecated. Don't use it.")
        setattr(self, name, value)

    def _reg_param(self, name):
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        """Deprecated."""
        warn("Worker._reg_param() is deprecated. Don't use it.")


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

    descr = property(get_descr, set_descr, doc="Description of work")

    def set_worker(self, act):
        """Set worker for doing work. Worker must be callable."""
        self._worker = act

    def __call__(self, *args, **kwargs):
        """Do work."""
        res = self._worker(*args, **kwargs)
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
        worker_params = worker_settings['params'].copy()

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
