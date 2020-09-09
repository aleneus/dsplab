"""Workers for examples."""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Activity


class Linear(Activity):
    """Linear transformation: y = k*x + b."""
    def __init__(self, k, b):
        super().__init__()
        self.k = k
        self.b = b

    def __call__(self, x):
        y = x*self.k + self.b
        return y


class Sum(Activity):
    """Sum."""
    def __call__(self, *xs):
        y = sum(xs)
        return y


class Inc(Activity):
    """Add 1 to value."""
    def __init__(self):
        super().__init__()

    def __call__(self, x):
        y = x + 1
        return y


class DoNothing(Activity):
    """Just pass input to output."""
    def __init__(self):
        super().__init__()

    def __call__(selfm, x):
        return x
