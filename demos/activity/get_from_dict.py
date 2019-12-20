"""Example of getting the work from dictionary."""

import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Activity, get_work_from_dict
from dsplab.helpers import pretty_json


class Linear(Activity):
    """Linear transformation."""
    def __init__(self, k, b):
        super().__init__()
        self.k = k
        self.b = b

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


main()
