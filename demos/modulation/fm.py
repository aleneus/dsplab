""" Example of frequency modulation. """

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import matplotlib.pyplot as plt
import numpy as np
from dsplab.modulation import freq_mod


def modulator(t):
    """ Return frequency value. """
    x = 0.05*t + 0.5
    return x


def main():
    """ Run example. """
    T = 10
    fs = 100
    a = 1
    phi = 0
    x, ph, t = freq_mod(
        length=T,
        sample_rate=fs,
        amp=a,
        func=modulator,
    )
    plt.subplot(211)
    plt.plot(t, x)
    plt.subplot(212)
    plt.plot(t, ph)
    plt.show()


if __name__ == "__main__":
    main()
