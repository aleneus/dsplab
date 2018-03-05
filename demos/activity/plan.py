import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

from dsplab.activity import Activity, Work, Node, Plan

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

if __name__ == "__main__":
    p = Plan()
    
    a = Work("Linear transformation")
    b = Work("Linear transformation")
    c = Work("Linear transformation")
    d = Work("Linear transformation")
    a.set_worker(Linear(1,1))
    b.set_worker(Linear(2,2))
    c.set_worker(Linear(3,3))
    d.set_worker(Linear(4,4))
    
    node_a = Node(work=a)
    node_b = Node(work=b, inputs=[node_a])
    node_c = Node(work=c, inputs=[node_b])
    node_d = Node(work=d, inputs=[node_b])
    
    p.add_node(node_a)
    p.add_node(node_b)
    p.add_node(node_c)
    p.add_node(node_d)

    x = 5
    y = p([x,])
    print(y)
