""" Node may not have inputs."""

import sys
import os
from random import randint
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import WorkNode, Plan


def gen():
    """Generate random number."""
    y = randint(1,10)
    print("gen -> {}".format(y))
    return y


def inc(x):
    """Increment."""
    y = x + 1
    print("{} -> inc -> {}".format(x, y))
    return y


def plus(x1, x2):
    """Sum of two numbers."""
    y = x1 + x2
    print("{}, {} -> plus -> {}".format(x1, x2, y))
    return y


def main():
    """Run example."""
    p = Plan()
    g = WorkNode(Work("Generate random number", gen))
    a = WorkNode(Work("Add 1", inc))
    b = WorkNode(Work("Summation", plus))
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
