import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Work
from dsplab.plan import Node, Plan

from random import randint

def gen():
    y = randint(1,10)
    print("gen -> {}".format(y))
    return y

def inc(x):
    y = x + 1
    print("{} -> inc -> {}".format(x, y))
    return y

def plus(x1, x2):
    y = x1 + x2
    print("{}, {} -> plus -> {}".format(x1, x2, y))
    return y

def main():
    p = Plan()
    g = Node(Work("Generate random number", gen))
    a = Node(Work("Add 1", inc))
    b = Node(Work("Summation", plus))
    p.add_node(g)
    p.add_node(a)
    p.add_node(b, inputs=[g, a])
    p.inputs = [a]
    p.outputs = [b]

    x = [1]
    print(x)
    y = p(x)
    print(y)

if __name__ == "__main__":
    main()
