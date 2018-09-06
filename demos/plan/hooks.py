import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Work
from dsplab.plan import Node

def func(x):
    return x + 1

def main():
    print("""
    Start and stop hooks.
    """)
    
    def f1(node):
        print("Node {} started".format(node))
    def f2(node):
        print("Node {} finished".format(node))
        
    n = Node(
        work=Work("Increment", worker=func),
    )
    n.set_start_hook(f1, n)
    n.set_stop_hook(f2, n)
    
    n(5)

if __name__ == "__main__":
    main()
