"""Mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import MapNode, PassNode, Plan
from workers import Linear


def main():
    """Run example."""
    plan = Plan()
    pass_node_1 = PassNode()
    plan.add_node(pass_node_1)
    pass_node_2 = PassNode()
    plan.add_node(pass_node_2)
    work = Work("Transformation")
    work.set_worker(Linear(1, 1))
    map_node = MapNode(work, inputs=[pass_node_1, pass_node_2])
    plan.add_node(map_node)
    
    plan.set_inputs([pass_node_1, pass_node_2])
    plan.set_outputs([map_node])
    res = plan([
        [1, 2, 3],
        [4, 5]
    ])
    print(res)


main()

