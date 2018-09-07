"""
Pack inputs to list.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.activity import Work
from dsplab.plan import PassNode, PackNode, Plan
from workers import *


def main():
    """Run example."""
    print(__doc__)
    plan = Plan()
    node_1 = PassNode()
    node_2 = PassNode()
    node_3 = PassNode()
    pack_node_1 = PackNode()
    pack_node_2 = PackNode()

    plan.add_node(node_1)
    plan.add_node(node_2)
    plan.add_node(node_3)
    plan.add_node(pack_node_1, inputs=[node_1, node_2])
    plan.add_node(pack_node_2, inputs=[node_2, node_3])

    plan.set_inputs([node_1, node_2, node_3])
    plan.set_outputs([pack_node_1, pack_node_2])

    print(plan([1,2,3]))

main()
