"""Construct the plan and delete one node linked to others."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Activity, Work
from dsplab.plan import Node, Translator, Plan

def main():
    print(__doc__)
    p = Plan()
    a = Node()
    b = Node()
    c = Node()
    d = Node()
    p.add_node(a)
    p.add_node(b)
    p.add_node(c, inputs=[a])
    p.add_node(d, inputs=[a, b])

    print(d.inputs)

    p.remove_node(a)
    print(c.inputs)
    print(d.inputs)

    try:
        p.remove_node(a) # must raise an exception
    except RuntimeError as ex:
        print(ex)

if __name__ == "__main__":
    main()