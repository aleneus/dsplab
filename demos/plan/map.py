"""Mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import MapNode, Plan
from workers import Linear


def main():
    """Run example."""
    work = Work("Transformation")
    work.set_worker(Linear(1, 1))
    plan = Plan()
    node = MapNode(work)
    plan.add_node(node)
    plan.set_inputs([node])
    plan.set_outputs([node])
    res = plan([[1, 2, 3], ])
    print(res)


main()

