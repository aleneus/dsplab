"""Online plan."""

from workers import Inc
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from dsplab.plan import Plan, WorkNode
from dsplab.activity import Work


def main():
    """Run example."""
    node_1 = WorkNode(work=Work("Step 1", worker=Inc()))
    node_2 = WorkNode(work=Work("Step 2", worker=Inc()))
    node_3 = WorkNode(work=Work("Step 3", worker=Inc()))
    plan = Plan(quick=True)
    plan.add_node(node_1)
    plan.add_node(node_2, inputs=[node_1])
    plan.add_node(node_3, inputs=[node_2])
    plan.set_inputs([node_1])
    plan.set_outputs([node_3])

    xs = [1, 2, 3, 4, 5]
    for x in xs:
        y = plan([x])[0]
        print("{} -> {}".format(x, y))

if __name__ == "__main__":
    main()