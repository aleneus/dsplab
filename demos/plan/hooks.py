"""Start and stop hooks."""
from dsplab.activity import Work
from dsplab.plan import WorkNode, Plan


def func(x):
    """Worker."""
    return x + 1


def start_handler(node):
    """Node start handler."""
    print("'{}' started".format(node.work.descr))


def stop_handler(node):
    """Node stop handler."""
    print("'{}' finished".format(node.work.descr))


def progress_handler():
    """Progress handler."""
    print("Calculated one node.")


def main():
    """Entry point."""
    print(__doc__)
    node = WorkNode(work=Work("Increment", worker=func))
    node.set_start_hook(start_handler, node)
    node.set_stop_hook(stop_handler, node)
    plan = Plan()
    plan.add_node(node)
    plan.set_progress_hook(progress_handler)
    plan.inputs = [node]
    plan.outputs = [node]
    plan([5])


if __name__ == "__main__":
    main()
