"""Work example."""
from dsplab.activity import Activity, Work


class MyWork(Activity):
    """Some work."""
    def __init__(self, k):
        super().__init__()
        self.k = k

    def __call__(self, x):
        return x + self.k


def main():
    """Entry point."""
    wk1 = MyWork(1)
    wk2 = MyWork(2)
    transfrom = Work()

    transfrom.set_worker(wk1)
    print(transfrom(5))

    transfrom.set_worker(wk2)
    print(transfrom(5))

    transfrom.set_worker(lambda x: x**2)
    print(transfrom(5))


if __name__ == "__main__":
    main()
