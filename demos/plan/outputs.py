"""
User-specified outputs.

a -> b
b ->
b -> c ->
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
    a = WorkNode(work=Work("Linear transformation", worker=Linear(1,1)))
    b = WorkNode(work=Work("Linear transformation", worker=Linear(2,2)))
    c = WorkNode(work=Work("Linear transformation", worker=Linear(3,3)))
    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    p.outputs = [c, b]

    x = 5
    y = p([x])
    print(y)


main()
