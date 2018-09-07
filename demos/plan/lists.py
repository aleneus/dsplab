"""
Processing of lists.

a -> b -> c
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import WorkNode, Plan
from workers import *


def main():
    """Run example."""
    print(__doc__)

    p = Plan()
    
    a = WorkNode(work=Work("Transformation", worker=MultipleList(2)))
    b = WorkNode(work=Work("Transformation", worker=MultipleList(3)))
    c = WorkNode(work=Work("Transformation", worker=MultipleList(4)))

    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    
    x = [1,1,1,1,1]
    y = p([x,])
    print(y)


if __name__ == "__main__":
    main()
