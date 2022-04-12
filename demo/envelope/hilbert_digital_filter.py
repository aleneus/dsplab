"""Amplitude with Hilbert digital filter."""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.modulation import digital_hilbert_filter


def main():
    """Run example."""
    fs = 50
    f = 0.4
    T = 100
    t = np.linspace(0, T, (T-1)*fs)
    m = 2 + np.sin(2*np.pi*f/10*t)
    x = m * np.sin(2*np.pi*f*t)
    h = digital_hilbert_filter(201)
    xf = np.convolve(x, h, mode='same')

    env = np.abs(x + 1j*xf)

    plt.figure()
    plt.plot(t, x)
    plt.plot(t, env)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
