import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import matplotlib.pyplot as plt
import numpy as np
from dsplab.modulation import fm

def func(t):
    x = 0.05*t + 0.5
    return x

def main():
    T = 10
    fs = 100
    a = 1
    phi = 0
    x, t = fm(T, fs, a, phi, func)
    plt.plot(t, x)
    plt.show()

if __name__ == "__main__":
    main()
