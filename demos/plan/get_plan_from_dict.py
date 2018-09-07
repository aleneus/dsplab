"""Get plan from dictionary."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.plan import get_plan_from_dict
from workers import *


SETTINGS = {
    'descr': 'Three-step plan',
    'nodes': [
        {
            'id': 'a',
            'work': {
                'descr': "First step",
                'worker': {
                    'class': "Linear",
                    'params': {
                        'k': 1,
                        'b': 1,
                    }
                }
            }
        },

        {
            'id': 'b',
            'work': {
                'descr': "Second step",
                'worker': {
                    'function': "numpy.exp"
                }
            },
            'inputs': ['a'],
        },

        {
            'id': 'c',
            'work': {
                'descr': "Third step",
                'worker': {
                    'class': "Inc"
                }
            },
            'inputs': ['b'],
        }
    ],

    'inputs': ['a'],
    'outputs': ['b', 'c'],
}


def main():
    """Run example."""
    plan = get_plan_from_dict(SETTINGS)
    x = 1
    y = plan([x])
    print(y)
    print()
    print(plan.info(as_string=True))


if __name__ == "__main__":
    main()
