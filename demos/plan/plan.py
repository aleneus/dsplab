import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

from dsplab.activity import Activity, Work
from dsplab.plan import Node, Transmitter, Plan

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
    work_a = Work("Linear transformation")
    work_b = Work("Linear transformation")
    work_c = Work("Linear transformation")
    work_d = Work("Linear transformation")
    
    work_a.set_worker(Linear(1,1))
    work_b.set_worker(Linear(2,2))
    work_c.set_worker(Linear(3,3))
    work_d.set_worker(Linear(4,4))
    
    a = Node(work=work_a)
    b = Node(work=work_b)
    c = Node(work=work_c)
    d = Node(work=work_d)

    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    p.add_node(d, inputs=[b])

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
    b = Node(work=Work("Transformation", worker=Linear(2,2)))
    c = Node(work=Work("Transformation", worker=Linear(3,3)))
    d = Node(work=Work("Merging", worker=Sum()))

    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[a])
    p.add_node(d, inputs=[b,c])
    
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
    b = Node(work=Work("Transformation", worker=MultipleList(3)))
    c = Node(work=Work("Transformation", worker=MultipleList(4)))

    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    
    x = [1,1,1,1,1]
    y = p([x,])
    print(y)

def example_4():
    print("""
    Example 4. User-specified outputs.

    a -> b
    b ->
    b -> c ->
    """)
    p = Plan()
    a = Node(work=Work("Linear transformation", worker=Linear(1,1)))
    b = Node(work=Work("Linear transformation", worker=Linear(2,2)))
    c = Node(work=Work("Linear transformation", worker=Linear(3,3)))
    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    p.outputs = [c, b]

    x = 5
    y = p([x])
    print(y)

def example_5():
    print("""
    Example 6. Start and stop hooks.
    """)
    
    def f1():
        print("Node started")
    def f2():
        print("Node finished")
        
    n = Node(
        work=Work("Linear transformation", worker=Linear(1,1)),
        start_hook = f1,
        stop_hook = f2,
    )
    
    n(5)

if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()
    example_5()
