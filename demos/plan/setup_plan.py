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

class Inc(Activity):
    def __init__(self):
        super().__init__()
    
    def __call__(self, x):
        y = x + 1
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
            # 'input' : True,
            # 'output': True,
        },
        {
            'id': 'b',
            'work': {
                'descr': "Second step",
                'worker': {
                    # is a function
                    'function': "numpy.exp"
                }
            },
            'inputs' : ['a'],
            'output' : True,
        },
        {
            'id': 'c',
            'work': {
                'descr': "Third step",
                'worker': {
                    # is a class with no args in init
                    'class': "Inc"
                }
            },
            'inputs' : ['b'],
            'output' : True,
        }
    ]
    
    p = Plan()
    if not setup_plan(p, nodes_settings):
        print('Error in settings')
        return
    x = 1
    y = p([x])
    print(y)

def example_2():
    
    settings = {
        'nodes' : [
            {
                'id' : 'a',
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
                'inputs' : ['a'],
            },

            {
                'id': 'c',
                'work': {
                    'descr': "Third step",
                    'worker': {
                        'class': "Inc"
                    }
                },
                'inputs' : ['b'],
            }
        ],
        
        'inputs': ['a'],
        'outputs': ['b', 'c'],
    }
    
    p = Plan()
    p.setup_from_dict(settings)
    x = 1
    y = p([x])
    print(y)

if __name__ == "__main__":
    example_2()
