"""Workers for examples."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Worker


class Linear(Worker):
    """Linear transformation: y = k*x + b."""
    def __init__(self, k, b):
        super().__init__()
        self.add_param('k', k)
        self.add_param('b', b)

    def __call__(self, x):
        y = x*self.k + self.b
        return y


class Sum(Worker):
    """ Sum. """
    def __call__(self, *xs):
        y = sum(xs)
        return y


class MultipleList(Worker):
    """ Multiple the elements of list by k. """
    def __init__(self, k):
        super().__init__()
        self.add_param('k', k)

    def __call__(self, x):
        y = [x_*self.k for x_ in x]
        return y


class Inc(Worker):
    def __init__(self):
        super().__init__()

    def __call__(self, x):
        y = x + 1
        return y
