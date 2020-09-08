"""Example of calculating amplitude by extremums."""
import matplotlib.pyplot as plt
import numpy as np
from dsplab.modulation import envelope_by_extremums


def main():
    """Run example."""
    fs = 50
    f = 0.2
    T = 60
    t = np.linspace(0, T, (T-1)*fs)
    e = np.exp(-t/10)
    x = np.sin(2*np.pi*f*t) * e

    env, t_env = envelope_by_extremums(x, sample_rate=fs)

    plt.figure()
    plt.plot(t, x)
    plt.plot(t_env, env)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
