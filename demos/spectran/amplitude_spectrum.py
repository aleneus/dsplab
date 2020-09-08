"""Amplitude spectrum example."""
import sys
import os

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath('.'))
from dsplab import spectran as sp


def main():
    """Run example."""
    sample_rate = 50
    freq_1 = 0.2
    freq_2 = 0.5
    freq_3 = 0.7
    freq_4 = 1.75

    T = 60
    ts = np.arange(0, T, 1/sample_rate)
    xs1 = np.sin(2 * np.pi * freq_1 * ts)
    xs2 = np.sin(2 * np.pi * freq_2 * ts)
    xs3 = np.sin(2 * np.pi * freq_3 * ts)
    xs4 = np.sin(2 * np.pi * freq_4 * ts)
    xs = xs1 + xs2 + xs3 + xs4

    X, fs = sp.spectrum(xs, sample_rate, one_side=True)

    plt.figure(figsize=(9, 9))

    plt.subplot(2, 1, 1)
    plt.plot(ts, xs)
    plt.xlabel("Time [sec]")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(fs, X)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
