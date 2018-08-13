""" Harmonics with noise. """

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import matplotlib.pyplot as plt
import numpy as np
import random
from dsplab.modulation import harm


def noise(t):
    """ Return random value. """
    x = random.normalvariate(0, 0.1)
    return x


def main():
    """ Run example. """
    T = 10
    fs = 100
    a = 1
    phi = 0
    x, t = harm(
        length=T, sample_rate=fs,
        amp=1, freq=1,
    )
    plt.plot(t, x)
    x, t = harm(
        length=T, sample_rate=fs,
        amp=2, freq=1,
        noise_a=noise
    )
    plt.plot(t, x)
    x, t = harm(
        length=T, sample_rate=fs,
        amp=2, freq=1,
        noise_f=noise
    )
    plt.plot(t, x)
    plt.show()


if __name__ == "__main__":
    main()
