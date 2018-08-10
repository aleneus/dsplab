import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Work
from dsplab.plan import Node, Plan

from workers import *

def main():
    print("""
    User-specified outputs.

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

main()
