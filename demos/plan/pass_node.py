"""Using Transmitter as input for part of data."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.plan import WorkNode, PassNode, Plan
from dsplab.activity import Work


def mul(x):
    """Worker."""
    return 2*x


def plus(x1, x2):
    """Another worker."""
    return x1 + x2


def main():
    """Run Example."""
    print(__doc__)
    plan = Plan()
    mul_node = WorkNode(work=Work("Mult", worker=mul))
    sum_node = WorkNode(work=Work("Sum", worker=plus))
    pass_node = PassNode()
    plan.add_node(mul_node)
    plan.add_node(pass_node)
    plan.add_node(sum_node, inputs=[mul_node, pass_node])
    print(plan([1, 2]))
    print(plan([2, 3]))

    
if __name__ == "__main__":
    main()
