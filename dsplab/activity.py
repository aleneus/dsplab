# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This module implements the base classes for offline and online
data processing tools. """

from collections import deque
import json
import numpy as np
from dsplab.helpers import import_entity


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
        print(res.__dict__)
        return res


class Activity(metaclass=ActivityMeta):
    """ Any activity -- something that may be called and can provide the
    information about itself. To get working activity you must
    implement __call__ method. """
    def __init__(self):
        """ Initialization. """
        self._info = self._class_info.copy()
        self._info['params'] = {}

    def set_descr(self, descr):
        """ Set description of activity. """
        self._info['descr'] = descr

    def add_param(self, name, value=None):
        """ Add parameter to activity and make record about it in info. """
        setattr(self, name, value)
        self._info['params'][name] = value

    def info(self, as_string=False):
        """ Return the information about activity.

        Parameters
        ----------
        as_string: bool
            Method returns JSON-string if True and dict otherwise

        Returns
        -------
        : str or dict
            Information about activity.

        """
        if as_string:
            return json.dumps(
                self._info,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        else:
            return self._info


class OnlineFilter(Activity):
    """ Base class for online filter. """
    def __init__(self, ntaps=None, smooth_ntaps=None, fill_with=0, step=1):
        """
        Initialization.

        Parameters
        ----------
        ntaps : int
            Length of internal queue using for accumulation of input
            samples. Default is None.
        smooth_ntaps : int
            Length of queue using for smoothing output values. Default
            id None.
        fill_with : float
            Initial value of every element of queues.
        step : int
            Step. Must be positive.

        """
        super().__init__()
        self.add_sample_func = None
        if (ntaps is None) and (smooth_ntaps is None):
            self.add_sample_func = self.__add_sample_simple
        elif (ntaps is not None) and (smooth_ntaps is None):
            self.add_sample_func = self.__add_sample_only_queue
        elif (ntaps is None) and (smooth_ntaps is not None):
            self.add_sample_func = self.__add_sample_only_smooth
        else:
            self.add_sample_func = self.__add_sample_full

        self.queue = None
        self.smooth_queue = None
        if ntaps is not None:
            self.queue = deque([fill_with]*ntaps, maxlen=ntaps)
        if smooth_ntaps is not None:
            self.smooth_queue = deque(
                [fill_with]*smooth_ntaps,
                maxlen=smooth_ntaps
            )
            wind = np.hamming(smooth_ntaps)
            self.wind = wind / sum(wind)

        self.step = step
        self.steps = 0

        self.ntaps = ntaps
        self.smooth_ntaps = smooth_ntaps

    def add_sample(self, value):
        """
        Add input sample to filter and return output value.

        Parameters
        ----------
        value : float
            Input value.

        Returns
        -------
        : float
            Output value.

        """
        return self.add_sample_func(value)

    def __call__(self, value):
        return self.add_sample_func(value)

    def __add_sample_simple(self, value):
        """ Add sample without using queues. """
        self.steps += 1
        if self.steps == self.step:
            self.steps = 0
            return self.proc_sample(value)
        return None

    def __add_sample_only_queue(self, value):
        """ Add sample with no smoothing. """
        self.steps += 1
        self.queue.append(value)
        if self.steps == self.step:
            self.steps = 0
            return self.proc_queue()
        return None

    def __add_sample_only_smooth(self, value):
        """ Add sample with not internal queue but with smoothed ouput. """
        self.steps += 1
        if self.steps == self.step:
            self.steps = 0
            self.smooth_queue.append(self.proc_sample(value))
            resm = np.dot(np.array(self.smooth_queue), self.wind)
            return resm
        return None

    def __add_sample_full(self, value):
        """ Add sample with internal queue and smoothing of ouput values. """
        self.steps += 1
        self.queue.append(value)
        if self.steps == self.step:
            self.steps = 0
            self.smooth_queue.append(self.proc_queue())
            resm = np.dot(np.array(self.smooth_queue), self.wind)
            return resm
        return None

    def proc_queue(self):
        """
        Process queue.

        Returns
        -------
        : float
            Ouput value.

        """
        pass

    def proc_sample(self, value):
        """
        Process sample.

        Parameters
        ----------
        x : float
            Input value.

        Returns
        -------
        : float
            Output value.

        """
        pass


class OnlineLogic(OnlineFilter):
    """ Base class for logical connectors of outputs of several
    detectors or other connectors. """
    def __init__(self, inputs=None):
        """
        Initialization.

        Parameters
        ----------
        inputs : list
            Input filters.

        """
        super().__init__()
        self._info['descr'] = 'Logical operation'
        self._info['inputs'] = []
        if inputs is None:
            self.inputs = []
        else:
            for inpt in inputs:
                self.add_input(inpt)

    def add_input(self, inpt):
        """ Add input of other connector.

        Parameters
        ----------
        inpt : Object
            Input.

        """
        self.inputs.append(inpt)
        self._info['inputs'].append(inpt.info())

    def add_sample(self, xs):
        raise NotImplementedError


class And(OnlineLogic):
    """ And connector. """
    def add_sample(self, values):
        result = 1
        for (inpt, value) in zip(self.inputs, values):
            result *= inpt.add_sample(value)
        return result


class Or(OnlineLogic):
    """ Or connector. """
    def add_sample(self, values):
        res = 0
        for (inpt, value) in zip(self.inputs, values):
            res += inpt.add_sample(value) * (1 - res)
        return res


class Work(Activity):
    """ Work is activity which has some worker. Different workers can
    be used for doing the same work. """
    def __init__(self, descr="", worker=None):
        """ Initialization. """
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


def get_work_from_dict(settings):
    """ Create and return Work instance setted from dictionary. """

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
        worker = import_entity(worker_name)(**worker_params)
    else:
        if key == 'class':
            worker = import_entity(worker_name)()
        else:
            worker = import_entity(worker_name)

    work = Work(descr, worker)
    return work
