"""Using of SelectNode with multiple input."""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from dsplab.flow.activity import Work
from dsplab.flow.plan import SelectNode, WorkNode, Plan
from workers import DoNothing


def main():
    """Run example."""
    plan = Plan()

    pass_node_1 = WorkNode(Work(descr="Pass", worker=DoNothing()))
    pass_node_2 = WorkNode(Work(descr="Pass", worker=DoNothing()))
    select_node_m = SelectNode(index=0)
    select_node_s = SelectNode(index=0)

    plan.add_node(pass_node_1)
    plan.add_node(pass_node_2)
    plan.add_node(select_node_m,
                  inputs=[pass_node_1, pass_node_2])
    plan.add_node(select_node_s,
                  inputs=[pass_node_1])
    plan.inputs = [pass_node_1, pass_node_2]
    plan.outputs = [select_node_m, select_node_s]

    res = plan([
        [1, 2, 3],
        [2, 3, 4]
    ])
    print("Outputs: ", res)


if __name__ == "__main__":
    main()
