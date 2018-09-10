"""Mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import MapNode, WorkNode, Plan
from workers import Linear, DoNothing


def main():
    """Run example."""
    plan = Plan()

    pass_node = WorkNode(
        Work("Pass", worker=DoNothing())
    )

    map_node = MapNode(
        work=Work("Transformation", worker=Linear(1,1)),
        inputs=[pass_node]
    )

    plan.add_node(pass_node)
    plan.add_node(map_node)
    plan.set_inputs([pass_node])
    plan.set_outputs([map_node])

    res = plan([
        [1, 2, 3],
    ])
    print(res)

main()

