import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Activity

class Linear(Activity):
    """ Linear transformation: y = k*x + b. """
    def __init__(self, k, b):
        super().__init__()
        self.k = k
        self.b = b
        self._info['params'] = {'k': k, 'b': b}

    def __call__(self, x):
        y = x*self.k + self.b
        return y

class Sum(Activity):
    """ Sum. """
    def __call__(self, *xs):
        y = sum(xs)
        return y

class MultipleList(Activity):
    """ Multiple the elements of list by k. """
    def __init__(self, k):
        super().__init__()
        self.k = k
        self._info['params'] = {'k': k}

    def __call__(self, x):
        y = [x_*self.k for x_ in x]
        return y
