import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from dsplab import envelope
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np

fs = 50
f = 0.4

rcParams['figure.figsize'] = 9, 6

T = 100
t = np.linspace(0, T, (T-1)*fs)
m = 2 + np.sin(2*np.pi*f/10*t)
x = m * np.sin(2*np.pi*f*t)
h = envelope.hilbert_filter(round(5*fs))
xf = np.convolve(x, h, mode = "same")
env = np.abs(x + 1j*xf)

plt.figure()
plt.plot(t, x)
plt.plot(t, env)
plt.tight_layout()
plt.savefig("hilbert-digital-filter.png")
