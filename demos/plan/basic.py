"""
Basic usage of plan.

a -> b
b -> c, d
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Work
from dsplab.plan import WorkNode, Plan

from workers import *


def main():
    print(__doc__)
    p = Plan()
    work_a = Work("Linear transformation")
    work_b = Work("Linear transformation")
    work_c = Work("Linear transformation")
    work_d = Work("Linear transformation")
    
    work_a.set_worker(Linear(1,1))
    work_b.set_worker(Linear(2,2))
    work_c.set_worker(Linear(3,3))
    work_d.set_worker(Linear(4,4))
    
    a = WorkNode(work=work_a)
    b = WorkNode(work=work_b)
    c = WorkNode(work=work_c)
    d = WorkNode(work=work_d)

    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    p.add_node(d, inputs=[b])

    x = 5
    y = p([x])
    print(y)

main()
