"""Pack inputs to list."""
from dsplab.activity import Work
from dsplab.plan import WorkNode, PackNode, Plan
from workers import DoNothing


def main():
    """Run example."""
    print(__doc__)
    plan = Plan()
    node_1 = WorkNode(Work("Pass", worker=DoNothing()))
    node_2 = WorkNode(Work("Pass", worker=DoNothing()))
    node_3 = WorkNode(Work("Pass", worker=DoNothing()))
    pack_node_1 = PackNode()
    pack_node_2 = PackNode()

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
