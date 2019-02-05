"""Example of getting the work from dictionary."""

import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Worker
from dsplab.activity import get_work_from_dict


class Linear(Worker):
    """Linear transformation."""
    def __init__(self, k, b):
        super().__init__()
        self.add_param('k', k)
        self.add_param('b', b)

    def __call__(self, x):
        y = x*self.k + self.b
        return y


def main():
    """Entry point."""
    work_settings = {
        'descr': 'Transformation',
        'worker': {
            'class': 'Linear',
            'params': {
                'k': 2,
                'b': 3,
            }
        }
    }
    transfrom = get_work_from_dict(work_settings)
    x = 11
    y = transfrom(x)
    print(y)
    print()
    print(transfrom.info(as_string=True))


main()
