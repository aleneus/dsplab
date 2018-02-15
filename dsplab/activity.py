""" This module implements the base classes for offline and online data processing tools. """

from collections import deque
import json
import numpy as np

def pretty_json_string(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

class Activity:
    def __init__(self):
        self.intermed = {}
    
    def info(self):
        return ""
    
    def __call__(self):
        raise NotImplementedError

class OnlineFilter(Activity):
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

    def info(self):
        # TODO: implement
        pass

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

    def __call__(self):
        # TODO: doc
        # TODO: [1] refactor add_sample and __call__ pair
        return self.add_sample()

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
    
class OnlineLogic(OnlineFilter):
    """ Base class for logical connectors of outputs of several detectors or other connectors. """
    def __init__(self, inputs=[]):
        """ 
        Initialization.

        Parameters
        ----------
        inputs : list
            Input filters.

        """
        self.inputs = inputs

    def info(self, as_string=False):
        d = {}
        d['class'] = self.__class__.__name__
        d['descr'] = 'Logical operation'
        d['inputs'] = [] # TODO: discuss about key name
        for inpt in self.inputs:
            det_info = inpt.info()
            d['inputs'].append(det_info)
        return pretty_json_string(d) if as_string else d

    def add_input(self, inpt):
        """ Add input of other connector.

        Parameters
        ----------
        inpt : Object
            Input.

        """
        self.inputs.append(inpt)

    def add_sample(self, xs):
        raise NotImplementedError

class And(OnlineLogic):
    """ And connector. """
    def add_sample(self, xs):
        result = 1
        for (inpt, x) in zip(self.inputs, xs):
            result *= inpt.add_sample(x)
        return result

class Or(OnlineLogic):
    """ Or connector. """
    def add_sample(self, xs):
        res = 0
        for (inpt, x) in zip(self.inputs, xs):
            res += inpt.add_sample(x) * (1 - res)
        return res
    
class Strategy(Activity):
    # TODO: doc
    def __init__(self, name="", info=""):
        """ Initialization. """
        self.name = name
        self.info = info
        self.intermed = {}
        self.workers = {}

    def set_worker(self, work, worker):
        """
        Add worker.
        
        Parameters
        ----------
        work : str
            Name of work.
        worker : object
            Worker object.
        
        """
        self.workers[work] = worker

    def set_default_worker(self, work, worker):
        """
        Set default worker.

        Parameters
        ----------
        work : str
            Name of work.
        worker : object
            Worker object.

        """
        if not work in self.workers.keys():
            self.workers[work] = worker
        
    def collect_workers_info(self, works, splitter='\n'):
        """
        Collect information from workers.

        Parameters
        ----------
        works : list of str
            Interested works.
        splitter : str
            Splitter between desctriprions of works.

        Return
        ------
        workers_info : str
            Collected information.

        """
        workers_info = ""
        for work in works:
            workers_info += splitter+self.workers[work].info+splitter
        return workers_info

    def info(self):
        # TODO: refact collect_workers_info and info pair
        return collect_workers_info()

    def __call__(self):
        """ Start activity. """
        raise NotImplementedError

