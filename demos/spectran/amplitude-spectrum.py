import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from dsplab import spectran as sp
import matplotlib.pyplot as plt
import numpy as np

fs = 50
f1 = 0.2
f2 = 0.5
f3 = 0.7
f4 = 2.11

T = 60
t = np.arange(0, T, 1/fs)
x1 = np.sin(2*np.pi*f1*t)
x2 = np.sin(2*np.pi*f2*t)
x3 = np.sin(2*np.pi*f3*t)
x4 = np.sin(2*np.pi*f4*t)
x = x1 + x2 + x3 + x4

X = sp.spectrum(x)

# plotting
plt.figure(figsize=(9, 6))

plt.subplot(2,1,1)
plt.plot(t,x)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(2,1,2)
f = np.fft.fftfreq(len(X), 1/fs)
ind = (f>=0) & (f<=5)
plt.plot(f[ind], (2*X/len(X))[ind])
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.grid(True)

plt.savefig("amplitude-spectrum.png")
