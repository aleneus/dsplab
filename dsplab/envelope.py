# Copyright (C) 2017 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from scipy.signal import hilbert

def envelope_by_extremums(x, fs = 1, t = []):
    """ 
    Calculate envelope by local extremums of signals

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency
    t : array_like
        Time values. Use it for unregular discretized input signal

    Returns
    --------
    
    x_new : np.array
        Damping values
    t_new : np.array
        Time values

    """
    if len(t) == 0:
        t = np.linspace(0, (len(x)-1)/fs, len(x))
    t_new = []
    x_new = []
    x = abs(x)
    for x_left, x_central, x_right, t_central in zip(x[:-2], x[1:-1], x[2:], t[1:-1]):
        if (x_left < x_central) and (x_central >= x_right):
            t_new.append(t_central)
            x_new.append(x_central)
    if x[-1] > x[-2]:
        t_new.append(t[-1])
        x_new.append(x[-1])
    return np.array(x_new), np.array(t_new)

def envelope_hilbert(x, fs = 1):
    """ 
    Calculate envelope using Hilbert transform


    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency

    Returns
    --------
    
    x_new : np.array
        Damping values

    """
    analytic = hilbert(x)
    x_new = np.abs(analytic)
    return x_new
