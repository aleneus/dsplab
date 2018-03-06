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

class Sum(Activity):
    def __init__(self):
        super().__init__()
        self._info['descr'] = "Sum"

    def __call__(self, xs):
        y = sum(xs)
        return y

class MultipleList(Activity):
    def __init__(self, k):
        super().__init__()
        self.k = k
        self._info['descr'] = "Multiple the elements of list by k"
        self._info['params'] = {'k': k}

    def __call__(self, x):
        y = [x_*self.k for x_ in x]
        return y

def example_1():
    print("""
    Example 1

    a -> b
    b -> c, d
    """)
    
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

    for node in [node_a, node_b, node_c, node_d]:
        p.add_node(node)

    x = 5
    y = p([x])
    print(y)

def example_2():
    print("""
    Example 2

    a -> b, c
    c, d -> d
    """)
    
    p = Plan()
    a = Node(work=Work("Transformation", worker=Linear(1,1)))
    b = Node(work=Work("Transformation", worker=Linear(2,2)), inputs=[a])
    c = Node(work=Work("Transformation", worker=Linear(3,3)), inputs=[a])
    d = Node(work=Work("Merging", worker=Sum()), inputs=[b,c])
    for node in [a,b,c,d]:
        p.add_node(node)
    x = 5
    y = p([x])
    print(y)

def example_3():
    print("""
    Example 3. Processing of lists

    a -> b -> c
    """)

    p = Plan()
    a = Node(work=Work("Transformation", worker=MultipleList(2)))
    b = Node(work=Work("Transformation", worker=MultipleList(3)), inputs=[a])
    c = Node(work=Work("Transformation", worker=MultipleList(4)), inputs=[b])
    for node in [a,b,c]:
        p.add_node(node)
    x = [1,1,1,1,1]
    y = p([x,])
    print(y)

if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
