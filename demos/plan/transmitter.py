""" Using Transmitter as input for part of data. """

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.plan import Node, Transmitter, Plan

def mul(x):
    return 2*x

def plus(x):
    return sum(x)

def main():
    p = Plan()
    a = Node(work=Work("Mult", worker=mul))
    b = Node(work=Work("Sum", worker=plus))
    t = Transmitter()
    x1 = 1
    x2 = 2
    p.add_node(a)
    p.add_node(t)
    p.add_node(b, inputs=[a,t])
    y = p([x1, x2])
    print(y)
    
if __name__ == "__main__":
    main()
