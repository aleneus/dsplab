import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Work
from dsplab.plan import Node, Plan

def func(x):
    return x + 1

def main():
    print("""
    Start and stop hooks.
    """)
    
    def f1():
        print("Node started")
    def f2():
        print("Node finished")
        
    n = Node(
        work=Work("Increment", worker=func),
        start_hook = f1,
        stop_hook = f2,
    )
    
    n(5)

if __name__ == "__main__":
    main()
