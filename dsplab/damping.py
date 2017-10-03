# Copyright (C) 2017 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np

def damping_triangles(x, fs = 1, t = []):
    """
    Calculate damping using triangle approximation

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency
    t : array_like
        Time values. Use it for unregular discretized input signal

    Rreturns
    --------
    
    ds : np.array
        Damping values
    ts : np.array
        Time values

    """
    ts = []
    ds = []

    if len(x) == 0:
        return ts, ds

    if len(t) == 0:
        t = np.linspace(0, (len(x)-1)/fs, len(x))

    def calc_one_value(t1, t2, x1, x2):
        ts.append(t2)
        ds.append((t2 - t1) / (x1 - x2))

    t_start = t[0]
    x_start = x[0]
    for x_prev, x_current, x_next, t_current in zip(x[:-2], x[1:-1], x[2:], t[1:-1]):
        if (x_prev <= x_current) and (x_current > x_next):
            t_start = t_current
            x_start = x_current
        if (x_prev > x_current) and (x_current <= x_next):
            t_stop = t_current
            x_stop = x_current
            calc_one_value(t_start, t_stop, x_start, x_stop)
    if x[-2] > x[-1]:
        t_stop = t[-1]
        x_stop = x[-1] 
        calc_one_value(t_start, t_stop, x_start, x_stop)
    return np.array(ds), np.array(ts)
