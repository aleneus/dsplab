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
    """Sum."""
    def __call__(self, *xs):
        y = sum(xs)
        return y


class Inc(Worker):
    """Add 1 to value."""
    def __init__(self):
        super().__init__()

    def __call__(self, x):
        y = x + 1
        return y


class DoNothing(Worker):
    """Just pass input to output."""
    def __init__(self):
        super().__init__()

    def __call__(selfm, x):
        return x
