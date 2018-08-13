""" Examle of amplitude modulation. """

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import matplotlib.pyplot as plt
import numpy as np
from dsplab.modulation import amp_mod


def modulator(t):
    """ Return amplitude value. """
    if t < 5:
        return 1
    return 2


def main():
    """ Run example. """
    T = 10
    fs = 100
    f = 1
    phi = 0
    x, t = amp_mod(
        length=T,
        sample_rate=fs,
        freq=f,
        func=modulator,
    )
    plt.plot(t, x)
    plt.show()


if __name__ == "__main__":
    main()
