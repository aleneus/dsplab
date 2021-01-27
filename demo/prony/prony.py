"""Prony decomposition example."""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath('.'))
from dsplab import prony


def main():
    """Entry point."""
    fs = 50
    T = 60
    t = np.linspace(0, T, T*fs + 1)
    x = np.cos(2*np.pi*1*t) * np.exp(-0.2*t) + \
        np.cos(2*np.pi*2*t) * np.exp(-1*t)

    components = prony.prony_decomp(x, 4)[2]

    fig = plt.figure()
    gridspec = fig.add_gridspec(2, len(components) // 2)
    fig.add_subplot(gridspec[0, :])

    plt.plot(x)
    plt.grid(True)

    for i, comp in enumerate(components):
        if i % 2 == 1:
            continue
        fig.add_subplot(gridspec[1, i // 2])
        plt.plot(comp)
        plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
