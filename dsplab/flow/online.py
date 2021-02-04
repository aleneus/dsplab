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

"""This module implements the base class for online filters."""

from math import pi
from collections import deque
import numpy as np
from dsplab.flow.activity import Activity

PI = pi
PI2 = 2 * PI


def unwrap_point(phi):
    """Unwrap angle (for signle value)."""
    if phi < -pi:
        return phi + (1 + int(phi / -pi)) * pi
    if phi > pi:
        return phi - (1 + int(phi / pi)) * pi
    return phi


class QueueFilter(Activity):
    """Online filter with queue.

    Parameters
    ----------
    ntaps: int
        Lenght of filter.
    fill_with: object
        Initial value of every element of queue.
    """
    def __init__(self, ntaps, fill_with=0):
        super().__init__()
        self.queue = deque([fill_with]*ntaps, maxlen=ntaps)
        self.ntaps = ntaps

    def __call__(self, *args, **kwargs):
        """Add sample to queue."""
        return self.__call(*args, **kwargs)

    def __call(self, sample):
        self.queue.append(sample)
        return self.proc_queue()

    def proc_queue(self):
        """Process queue."""
        raise NotImplementedError


class Delayer(QueueFilter):
    """Provide delay in online processing."""
    def proc_queue(self):
        return self.queue[0]


class And(Activity):
    """And operation."""
    def __call__(self, *args, **kwargs):
        """Do operation.

        Parameters
        ----------
        sample: array_like of floats
            Input values.
        """
        return self.__call(*args, **kwargs)

    def __call(self, sample):
        res = 1
        for value in sample:
            res *= value
        return res


class Or(Activity):
    """Or operation."""
    def __call__(self, sample):
        """Do operation.
        Parameters
        ----------
        sample: array_like of floats
            Input values.
        """
        res = 0
        for value in sample:
            res += value * (1 - res)
        return res


class OnlineFilter(Activity):
    """Universal online filter.

    Parameters
    ----------
    ntaps: int
        Length of internal queue using for accumulation of input
        samples. Default is None.
    smooth_ntaps: int
        Length of queue using for smoothing output values. Default
        id None.
    fill_with: object
        Initial value of every element of queues.
    step: int
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

    def __call__(self, *args, **kwargs):
        """Add input sample to filter and return output value.

        Parameters
        ----------
        sample: object
            Input sample.

        Returns
        -------
        : object
            Output value.
        """
        self.__call(*args, **kwargs)

    def __call(self, sample):
        return self.add_sample_func(sample)

    def __add_sample_simple(self, sample):
        """Add sample without using queues."""
        self.steps += 1
        if self.steps == self.step:
            self.steps = 0
            return self.proc_sample(sample)
        return None

    def __add_sample_only_queue(self, sample):
        """Add sample with no smoothing."""
        self.steps += 1
        self.queue.append(sample)
        if self.steps == self.step:
            self.steps = 0
            return self.proc_queue()
        return None

    def __add_sample_only_smooth(self, sample):
        """Add sample with not internal queue but with smoothed
        ouput."""
        self.steps += 1
        if self.steps == self.step:
            self.steps = 0
            self.smooth_queue.append(self.proc_sample(sample))
            resm = np.dot(np.array(self.smooth_queue), self.wind)
            return resm
        return None

    def __add_sample_full(self, sample):
        """Add sample with internal queue and smoothing of ouput
        values."""
        self.steps += 1
        self.queue.append(sample)
        if self.steps == self.step:
            self.steps = 0
            self.smooth_queue.append(self.proc_queue())
            resm = np.dot(np.array(self.smooth_queue), self.wind)
            return resm
        return None

    def proc_queue(self):
        """Process queue.

        Returns
        -------
        : object
            Ouput value.
        """

    def proc_sample(self, sample):
        """Process sample.

        Parameters
        ----------
        sample: object
            Input sample.

        Returns
        -------
        : object
            Output value.
        """
