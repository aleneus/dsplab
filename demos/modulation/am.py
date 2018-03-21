import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import matplotlib.pyplot as plt
import numpy as np
from dsplab.modulation import am

def func(t):
    if t < 5:
        return 1
    return 2

def main():
    T = 10
    fs = 100
    f = 1
    phi = 0
    x, t = am(T, fs, f, phi, func)
    plt.plot(t, x)
    plt.show()

if __name__ == "__main__":
    main()
