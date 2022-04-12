"""Workers for examples."""
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.flow.activity import Activity


class Linear(Activity):
    """Linear transformation: y = k*x + b."""
    def __init__(self, k, b):
        super().__init__()
        self.k = k
        self.b = b

    def __call__(self, x):
        return x*self.k + self.b


class Sum(Activity):
    """Sum."""
    def __call__(self, *xs):
        return sum(xs)


class Inc(Activity):
    """Add 1 to value."""
    def __init__(self):
        super().__init__()

    def __call__(self, x):
        return x + 1


class DoNothing(Activity):
    """Just pass input to output."""
    def __init__(self):
        super().__init__()

    def __call__(self, x):
        return x
