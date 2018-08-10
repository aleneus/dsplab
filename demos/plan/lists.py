import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.activity import Work
from dsplab.plan import Node, Plan

from workers import *

def main():
    print("""
    Processing of lists

    a -> b -> c
    """)

    p = Plan()
    
    a = Node(work=Work("Transformation", worker=MultipleList(2)))
    b = Node(work=Work("Transformation", worker=MultipleList(3)))
    c = Node(work=Work("Transformation", worker=MultipleList(4)))

    p.add_node(a)
    p.add_node(b, inputs=[a])
    p.add_node(c, inputs=[b])
    
    x = [1,1,1,1,1]
    y = p([x,])
    print(y)

if __name__ == "__main__":
    main()
