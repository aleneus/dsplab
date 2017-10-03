import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from dsplab import damping, envelope
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np

fs = 50
f = 0.2

rcParams['figure.figsize'] = 6, 6
plt.figure()

T = 60
t = np.linspace(0, T, (T-1)*fs)
e = np.exp(-t/10)
x = np.sin(2*np.pi*f*t) * e
env, t_env = envelope.envelope_by_max(x, fs = fs)
ds, ts = damping.damping_triangles(env, t = t_env)

plt.subplot(211)
plt.plot(t, x)
plt.plot(t_env, env)
plt.title("Damping = {}".format(ds[0]))

T = 120
t = np.linspace(0, T, (T-1)*fs)
e = np.exp(-t/10)
x = np.sin(2*np.pi*f*t) * e
env, t_env = envelope.envelope_by_max(x, fs = fs)
ds, ts = damping.damping_triangles(env, t = t_env)

plt.subplot(212)
plt.plot(t, x)
plt.plot(t_env, env)
plt.title("Damping = {}".format(ds[0]))

plt.tight_layout()
plt.savefig("x.png")
