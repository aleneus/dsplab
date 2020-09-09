"""Construct the plan and delete one node linked to others."""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from dsplab.plan import WorkNode, Plan


def main():
    """Run example."""
    print(__doc__)
    p = Plan()
    a = WorkNode()
    b = WorkNode()
    c = WorkNode()
    d = WorkNode()
    p.add_node(a)
    p.add_node(b)
    p.add_node(c, inputs=[a])
    p.add_node(d, inputs=[a, b])

    print(d.inputs)

    p.remove_node(a)
    print(c.inputs)
    print(d.inputs)

    try:
        p.remove_node(a)  # must raise an exception
    except RuntimeError as ex:
        print(ex)


if __name__ == "__main__":
    main()
