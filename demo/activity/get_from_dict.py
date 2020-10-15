"""Example of getting the work from dictionary."""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from dsplab.flow.activity import Activity, get_work_from_dict


class Mul(Activity):
    """Multiplies argument to parameter."""
    def __init__(self, p):
        super().__init__()
        self.p = p

    def __call__(self, x):
        return x * self.p


def main():
    """Entry point."""
    work_settings = {
        'descr': 'Transformation',
        'worker': {
            'class': 'Mul',
            'params': {'p': 2}
        }
    }
    transfrom = get_work_from_dict(work_settings)
    print(transfrom(11))


if __name__ == "__main__":
    main()
