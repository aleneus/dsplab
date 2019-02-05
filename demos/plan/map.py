"""Mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import MapNode, WorkNode, Plan
from workers import Sum, DoNothing


def main():
    """Run example."""
    plan = Plan()

    pass_node_1 = WorkNode(
        Work("Pass", worker=DoNothing())
    )
    pass_node_2 = WorkNode(
        Work("Pass", worker=DoNothing())
    )

    map_node = MapNode(
        work=Work("Transformation", worker=Sum()),
        inputs=[pass_node_1, pass_node_2]
    )

    plan.add_node(pass_node_1)
    plan.add_node(pass_node_2)
    plan.add_node(map_node)
    plan.inputs = [pass_node_1, pass_node_2]
    plan.outputs = [map_node]

    res = plan([
        [1, 1, 1],
        [2, 2, 2],
    ])
    print("Outputs:", res)


main()
