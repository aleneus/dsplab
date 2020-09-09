"""Smooth signal example."""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath('.'))
from dsplab.filtration import trend_smooth


def main():
    """Entry point."""
    fs = 50         # Hz
    T = 2*60        # sec
    f1 = 0.01       # Hz
    f2 = 0.1        # Hz
    f3 = 1          # Hz
    cut_off = 0.03  # Hz
    t = np.arange(0, T, 1/fs)
    x = np.cos(2*np.pi*f1*t) + np.cos(2*np.pi*f2*t) + np.cos(2*np.pi*f3*t)

    res = trend_smooth(xdata=x, tdata=t, cut_off=cut_off)
    if res is None:
        exit()

    trend_x, trend_t = res

    plt.plot(t, x)
    plt.plot(trend_t, trend_x)
    plt.show()


if __name__ == "__main__":
    main()
