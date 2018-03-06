""" This module implements the base classes for offline and online data processing tools. """

# TODO: add demos for info

from collections import deque, OrderedDict
import json
import numpy as np

class Activity:
    """ Any activity. Something that may be called and can provide the
    information about itself. """
    def __init__(self):
        """ Initialization. """
        self._info = {}
        self._info['class'] = self.__class__.__name__
    
    def info(self, as_string=False):
        """ Return the information about activity. 
        
        Parameters
        ----------
        as_string: bool
            Method returns JSON-string if True and dict overwise.

        Returns
        -------
        : str or dict
            Information about activity.

        """
        if as_string:
            return json.dumps(self._info, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return self._info
    
    def __call__(self):
        """ Act. """
        raise NotImplementedError

class OnlineFilter(Activity):
    """ Base class for online filter. """
    def  __init__(self, ntaps=None, smooth_ntaps=None, fill_with=0, step=1):
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
        # TODO: add arguments to self._info
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
        # TODO: depracate, use __call__
        return self.add_sample_func(x)

    def __call__(self, x):
        return self.add_sample(x)

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
    """ Base class for logical connectors of outputs of several
    detectors or other connectors. """
    # TODO: test info
    def __init__(self, inputs=[]):
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
        self.inputs = []
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

class Work(Activity):
    """ Work is activity which has some worker. Different workers can
    be used for doing the same work. """
    def __init__(self, descr="", worker=None):
        """ Initialization. """
        super().__init__()
        self.set_descr(descr)
        self.set_worker(worker)

    def set_descr(self, descr):
        """ Set description of work. """
        self.descr = descr
        self._info['descr'] = descr

    def set_worker(self, worker):
        """ Set worker for doing work. """
        self.worker = worker
        self._info['worker'] = None
        try:
            self._info['worker'] = worker.info()
        except:
            pass

    def __call__(self, *args, **kwargs):
        """ Do work. """
        y = self.worker(*args, *kwargs)
        return y

class Node:
    """ The node. Node can be understood as the workplace for
    worker. Node can have inputs that are also nodes. """
    def __init__(self, work=None, inputs=[]):
        """ Initialization. """
        self.work = work
        self._res = None
        self.set_inputs(inputs)

    def get_inputs(self):
        """ Return inputs. """
        return self._inputs
    def set_inputs(self, inputs):
        """ Set inputs. """
        self._inputs = inputs
    inputs = property(get_inputs, set_inputs)

    def is_output_ready(self) -> bool:
        """ Check if the calculation of data in the node is finished. """
        ans = self._res is not None
        return ans

    def is_inputs_ready(self) -> bool:
        """ Check if data in all inputs is ready. """
        for inpt in self._inputs:
            if not inpt.is_output_ready():
                return False
        return True

    def result(self):
        """ Return the calculated data. """
        return self._res

    def __call__(self, x=None):
        """ Run node. """
        if x is not None:
            y = self.work(x)
            self._res = y
            return
        
        self._res = None
        if len(self._inputs) == 1:
            x = self._inputs[0].result()
        else:
            x = [inpt.result() for inpt in self._inputs]
        y = self.work(x)
        self._res = y
    
class Plan:
    """ The plan. Plan is the system of linked nodes. """
    def __init__(self):
        """ Initialization. """
        super().__init__()
        self._nodes = []
        self._first_nodes = []
        self._last_nodes = []

    def _detect_terminals(self):
        """ Detect first and last nodes. """
        self._first_nodes = []
        all_inputs = []
        for node in self._nodes:
            if len(node.inputs) == 0:
                self._first_nodes.append(node)
            for inpt in node.inputs:
                if inpt not in all_inputs:
                    all_inputs.append(inpt)

        self._last_nodes = []
        for node in self._nodes:
            if node not in all_inputs:
                self._last_nodes.append(node)

    def add_node(self, node, inputs=[]):
        """ Add node to plan. """
        self._nodes.append(node)
        if len(inputs) > 0:
            node.inputs = inputs

    def __call__(self, xs):
        """ Run plan. """
        self._detect_terminals()
        for [node, x] in zip(self._first_nodes, xs):
            node(x)
        
        while True:
            finished = True
            for node in self._nodes:
                if not node.is_output_ready() and node.is_inputs_ready():
                    finished = False
                    node()
            if finished:
                break
        ys = [last_node.result() for last_node in self._last_nodes]
        return ys

class Strategy(Activity):
    """ Deprecated. """
    def __init__(self, name="", info=""):
        """ Initialization. """
        print("Deprecated: dsplab.activity.Strategy")
        self.name = name
        self.workers = OrderedDict()

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

    def __call__(self):
        raise NotImplementedError

class LinearStrategy(Strategy):
    """ Linear strategy. Works called one by one, from first setted
    work to the last one. """
    def __call__(self, x):
        y = x
        print(self.workers)
        for work in self.workers:
            y = self.workers[work](y)
        return y

if __name__ == "__main__":
    or_connector = Or()
    print(or_connector.info(as_string=True))
