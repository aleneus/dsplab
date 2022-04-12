"""Smooth signal example."""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.filtration import trend_smooth


def main():
    """Entry point."""
    period = 1 / 50  # sec
    length = 2 * 60  # sec

    freqs = [0.01, 0.1, 1]  # Hz
    cut_off = 0.03  # Hz

    t = np.arange(0, length, period)
    x = np.cos(2 * np.pi * freqs[0] * t)
    x += np.cos(2 * np.pi * freqs[1] * t)
    x += np.cos(2 * np.pi * freqs[2] * t)

    res = trend_smooth(xdata=x, tdata=t, cut_off=cut_off)
    if res is None:
        sys.exit(1)

    trend_x, trend_t = res

    plt.plot(t, x)
    plt.plot(trend_t, trend_x)
    plt.show()


if __name__ == "__main__":
    main()
