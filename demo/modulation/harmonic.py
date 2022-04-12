"""Harmonics with noise."""
import os
import sys
import random
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.modulation import harm


def noise():
    """Return random value."""
    return random.normalvariate(0, 0.1)


def main():
    """Run example."""
    T = 10
    fs = 100
    x, t = harm(
        length=T, sample_rate=fs,
        amp=1, freq=1,
    )
    plt.plot(t, x)
    x, t = harm(
        length=T, sample_rate=fs,
        amp=2, freq=1,
        noise_amp=noise
    )
    plt.plot(t, x)
    x, t = harm(
        length=T, sample_rate=fs,
        amp=2, freq=1,
        noise_ph=noise
    )
    plt.plot(t, x)
    plt.show()


if __name__ == "__main__":
    main()
