import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

from dsplab.activity import Activity
from dsplab.plan import Plan, setup_plan

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

def example():
    nodes_settings = [
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
            },
        },
        {
            'id': 'b',
            'work': {
                'descr': "Second step",
                'worker': {
                    'class': "numpy.exp"
                }
            },
            'inputs' : ['a']
        }
    ]
    p = Plan()
    setup_plan(p, nodes_settings)
    x = 1
    y = p([x])
    print(y)

if __name__ == "__main__":
    example()
