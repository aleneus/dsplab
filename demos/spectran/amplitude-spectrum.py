import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from dsplab import spectran as sp
from dsplab import filtration as flt
import matplotlib.pyplot as plt
import numpy as np

fs = 50
f1 = 0.2
f2 = 0.5
f3 = 0.7
f4 = 1.75

T = 60
t = np.arange(0, T, 1/fs)
x1 = np.sin(2*np.pi*f1*t)
x2 = np.sin(2*np.pi*f2*t)
x3 = np.sin(2*np.pi*f3*t)
x4 = np.sin(2*np.pi*f4*t)
x = x1 + x2 + x3 + x4

X, f_X = sp.spectrum(x, fs, one_side=True)

# plotting
plt.figure(figsize=(9, 9))

plt.subplot(2,1,1)
plt.plot(t,x)
plt.xlabel("Time [sec]")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(f_X, X)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.savefig("amplitude-spectrum.png")
