import numpy as np


def harmonic(T, fs, f, A=1, phi=0):
    """Generate harmonis signal."""
    t = np.linspace(0, T, T * fs + 1)
    x = A * np.cos(2 * np.pi * f * t + phi)

    return x, t
