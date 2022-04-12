"""Frequency  demodulation example."""
import sys
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import firwin

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.modulation import iq_demod


def main():
    """Entry point."""
    fs = 100

    t = np.arange(0, 10 * 60, 1.0 / fs)
    x = np.cos(2 * np.pi * 0.51 * t)

    band = [0.48, 0.53]
    f_central = sum(band) / 2
    width = (band[1] - band[0]) / 2
    b = firwin(12000, width, nyq=fs / 2, window="hamming")

    freq, t_freq = iq_demod(xdata=x,
                            tdata=t,
                            f_central=f_central,
                            a_coeffs=[1],
                            b_coeffs=b)

    print("Average frequency: {}".format(np.average(freq)))

    plt.plot(t_freq, freq)
    plt.ylim(band)
    plt.show()


if __name__ == "__main__":
    main()
