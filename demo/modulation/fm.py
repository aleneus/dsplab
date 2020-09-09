"""Example of frequency modulation."""
import os
import sys
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath('.'))
from dsplab.modulation import freq_mod


def modulator(t):
    """Return frequency value."""
    return 0.05*t + 0.5


def main():
    """Run example."""
    T = 10
    fs = 100
    amp = 1
    xs, phases, ts = freq_mod(
        length=T,
        sample_rate=fs,
        amp=amp,
        func=modulator,
    )
    plt.subplot(211)
    plt.plot(ts, xs)
    plt.subplot(212)
    plt.plot(ts, phases)
    plt.show()


if __name__ == "__main__":
    main()
