import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from dsplab import prony
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np

fs = 50
T = 60
t = np.linspace(0, T, T*fs + 1)
x = np.cos(2*np.pi*1*t) * np.exp(-0.2*t) + np.cos(2*np.pi*2*t) * np.exp(-1*t)

L = 4
ms, cs, es = prony.prony_decomp(x, L)

rcParams['figure.figsize'] = 6, 6
plt.figure()
plt.plot(x)
plt.grid(True)
plt.tight_layout()
plt.savefig("x.png")

rcParams['figure.figsize'] = 6, 12
plt.figure()
for i in range(L):
    plt.subplot(L*100 + 10 + i+1)
    plt.plot(es[i])
    plt.grid(True)
    
plt.tight_layout()
plt.savefig("decomp.png")
