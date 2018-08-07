import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

from dsplab.activity import Activity, Work

class Linear(Activity):
    """Linear transformation: y = k*x + b"""
    def __init__(self, k, b):
        super().__init__()
        self.add_param('k', k)
        self.add_param('b', b)

    def __call__(self, x):
        y = x*self.k + self.b
        return y

def sqr(x):
    y = x**2
    return y


if __name__ == "__main__":
    lin1 = Linear(1, 1)
    lin2 = Linear(2, 2)
    transfrom = Work('Some transformation')

    x = 5
    
    transfrom.set_worker(lin1)
    print(transfrom.info(as_string=True))
    print(transfrom(x))

    transfrom.set_worker(lin2)
    print(transfrom.info(as_string=True))
    print(transfrom(x))

    transfrom.set_worker(sqr)
    print(transfrom.info(as_string=True))
    print(transfrom(x))
