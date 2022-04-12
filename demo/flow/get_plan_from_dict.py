"""Get plan from dictionary."""
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.flow.plan import get_plan_from_dict

SETTINGS = {
    'nodes': [{
        'id': 'a',
        'class': 'WorkNode',
        'work': {
            'descr': "First step",
            'worker': {
                'class': "workers.Linear",
                'params': {
                    'k': 1,
                    'b': 1,
                }
            }
        }
    }, {
        'id': 'b',
        'class': 'WorkNode',
        'work': {
            'descr': "Second step",
            'worker': {
                'function': "numpy.exp"
            }
        },
        'inputs': ['a'],
    }, {
        'id': 'c',
        'class': 'WorkNode',
        'work': {
            'descr': "Third step",
            'worker': {
                'class': "workers.Inc"
            }
        },
        'inputs': ['b'],
    }, {
        'id': 'd',
        'class': 'PackNode',
        'inputs': ['b', 'c'],
        'result': 'Result value'
    }],
    'inputs': ['a'],
    'outputs': ['d'],
}


def main():
    """Run example."""
    plan = get_plan_from_dict(SETTINGS)
    x = 1
    y = plan([x])

    print(y)


if __name__ == "__main__":
    main()
