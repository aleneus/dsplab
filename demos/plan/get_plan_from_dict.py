import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

from dsplab.activity import Activity
from dsplab.plan import get_plan_from_dict


class Linear(Activity):
    def __init__(self, k, b):
        super().__init__()
        self.k = k
        self.b = b
        self._info['descr'] = "Linear transformation: y = k*x + b"
        self._info['params'] = {'k': k, 'b': b}

    def __call__(self, x):
        y = x*self.k + self.b
        return y


class Inc(Activity):
    def __init__(self):
        super().__init__()

    def __call__(self, x):
        y = x + 1
        return y


settings = {
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


plan = get_plan_from_dict(settings)
x = 1
y = plan([x])
print(y)
print()
print(plan.info(as_string=True))
