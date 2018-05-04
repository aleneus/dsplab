""" Using Transmitter as input for part of data. """

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.plan import Node, Transmitter, Plan
from dsplab.activity import Work

def mul(x):
    return 2*x

def plus(x1, x2):
    return x1 + x2

def main():
    p = Plan()
    a = Node(work=Work("Mult", worker=mul))
    b = Node(work=Work("Sum", worker=plus))
    t = Transmitter()
    p.add_node(a)
    p.add_node(t)
    p.add_node(b, inputs=[a,t])
    print(p([1, 2]))
    print(p([2, 3]))
    
if __name__ == "__main__":
    main()
