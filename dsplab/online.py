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

""" This module implements the base class for online filters. """

from math import pi
from collections import deque
import numpy as np
from dsplab.activity import Activity

PI = pi
PI2 = 2 * PI


def unwrap_point(w):
    """ Unwrap angle (for signle value). """
    if w < -PI:
        return w + PI2
    if w > PI:
        return w - PI2
    return w


class OnlineFilter(Activity):
    """Base class for online filter.

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
    def __init__(self, ntaps=None, smooth_ntaps=None, fill_with=0, step=1):
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
    """Base class for logical connectors of outputs of several
    detectors or other connectors.

    Parameters
    ----------
    inputs : list
        Input filters.
    """
    def __init__(self, inputs=None):
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
