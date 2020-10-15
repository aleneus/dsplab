"""Basic usage of plan."""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from dsplab.flow.activity import Work
from dsplab.flow.plan import WorkNode, Plan
from workers import Linear


def main():
    """Run example."""
    plan = Plan()
    node_a = WorkNode(work=Work("Linear transformation", worker=Linear(1, 1)))
    node_b = WorkNode(work=Work("Linear transformation", worker=Linear(2, 2)))
    node_c = WorkNode(work=Work("Linear transformation", worker=Linear(3, 3)))
    plan.add_node(node_a)
    plan.add_node(node_b, inputs=[node_a])
    plan.add_node(node_c, inputs=[node_b])
    plan.inputs = [node_a]
    plan.outputs = [node_c, node_b]

    print(plan([5]))


if __name__ == "__main__":
    main()
