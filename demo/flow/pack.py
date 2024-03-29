"""Pack inputs to list."""
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position,wrong-import-order,import-error
from dsplab.flow.activity import Work
from dsplab.flow.plan import WorkNode, PackNode, Plan
from workers import DoNothing


def main():
    """Run example."""
    print(__doc__)

    node_1 = WorkNode(Work("Pass", worker=DoNothing()))
    node_2 = WorkNode(Work("Pass", worker=DoNothing()))
    node_3 = WorkNode(Work("Pass", worker=DoNothing()))
    pack_node_1 = PackNode()
    pack_node_2 = PackNode()

    plan = Plan()

    plan.add_node(node_1)
    plan.add_node(node_2)
    plan.add_node(node_3)
    plan.add_node(pack_node_1, inputs=[node_1, node_2])
    plan.add_node(pack_node_2, inputs=[node_2, node_3])

    plan.inputs = [node_1, node_2, node_3]
    plan.outputs = [pack_node_1, pack_node_2]

    print(plan([1, 2, 3]))


if __name__ == "__main__":
    main()
