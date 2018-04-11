import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import matplotlib.pyplot as plt
import numpy as np
import random

from dsplab.modulation import harmonic

def noise(t):
    x = random.normalvariate(0, 0.1)
    return x

def main():
    T = 10
    fs = 100
    a = 1
    phi = 0
    x, t = harmonic(T=10, fs=100, a=1, f=1, ph=0)
    plt.plot(t, x)
    x, t = harmonic(T=10, fs=100, a=2, f=1, ph=0, noise_a=noise)
    plt.plot(t, x)
    x, t = harmonic(T=10, fs=100, a=1, f=2, ph=0, noise_f=noise)
    plt.plot(t, x)
    plt.show()

if __name__ == "__main__":
    main()
