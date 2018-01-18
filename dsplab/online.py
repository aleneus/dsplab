""" This module implements the base class for online filters. """

import numpy as np
from collections import deque

pi = np.pi
pi2 = 2*np.pi
e = np.exp(1)

def unwrap_point(w):
    """ Unwrap angle (for signle value). """
    if w < -pi:
        return w + pi2
    if w > pi:
        return w - pi2
    return w

class OnlineFilter:
    """ Base class for online filter. """
    def  __init__(self, ntaps=None, smooth_ntaps=None, fill_with=0, step=1):
        """ 
        Initialization.

        Parameters
        ----------
        ntaps : int
            Length of internal queue using for accumulation of input samples. Default is None.
        smooth_ntaps : int
            Length of queue using for smoothing output values. Default id None.
        fill_with : float
            Initial value of every element of queues.
        step : int
            Step. Must be positive.

        """
        self.add_sample_func = None
        if   (ntaps == None) and (smooth_ntaps == None):
            self.add_sample_func = self.__add_sample_simple
        elif (ntaps != None) and (smooth_ntaps == None):
            self.add_sample_func = self.__add_sample_only_queue
        elif (ntaps == None) and (smooth_ntaps != None):
            self.add_sample_func = self.__add_sample_only_smooth
        else:
            self.add_sample_func = self.__add_sample_full

        self.queue = None
        self.smooth_queue = None
        if ntaps!=None:
            self.queue = deque([fill_with]*ntaps, maxlen=ntaps)
        if smooth_ntaps!=None:
            self.smooth_queue = deque([fill_with]*smooth_ntaps, maxlen=smooth_ntaps)
            wind = np.hamming(smooth_ntaps)
            self.wind = wind / sum(wind)

        self.step = step
        self.steps = 0

        self.ntaps = ntaps
        self.smooth_ntaps = smooth_ntaps

    def add_sample(self, x):
        """
        Add input sample to filter and return output value.

        Parameters
        ----------
        x : float
            Input value.
        
        Returns
        -------
        : float
            Output value.

        """
        return self.add_sample_func(x)

    def __add_sample_simple(self, x):
        """ Add sample without using queues. """
        self.steps += 1
        if self.steps == self.step:
            self.steps = 0
            return self.proc_sample(x)
        return None

    def __add_sample_only_queue(self, x):
        """ Add sample with no smoothing. """
        self.steps += 1
        self.queue.append(x)
        if self.steps == self.step:
            self.steps = 0
            return self.proc_queue()
        return None

    def __add_sample_only_smooth(self, x):
        """ Add sample with not internal queue but with smoothed ouput. """
        self.steps += 1
        if self.steps == self.step:
            self.steps = 0
            self.smooth_queue.append(self.proc_sample(x))
            resm = np.dot(np.array(self.smooth_queue), self.wind)
            return resm
        return None

    def __add_sample_full(self, x):
        """ Add sample with internal queue and smoothing of ouput values. """
        self.steps += 1
        self.queue.append(x)
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
        raise NotImplementedError

    def proc_sample(self, x):
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
        raise NotImplementedError
