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

def freq_stupid(x, dt):
    """
    Calculate frequency of oscillating signal by extremums
    """
    T = len(x)*dt
    n_max = 0
    n_min = 0
    for x_prev, x_current, x_next in zip(x[:-2], x[1:-1], x[2:]):
        if (x_prev < x_current) and (x_current >= x_next):
            n_max += 1
        if (x_prev > x_current) and (x_current <= x_next):
            n_min += 1
    n = np.max([n_max, n_min])
    f = n / T
    return f

def freqs_stupid(x, dt, window_width = 100, window_step = 50):
    """
    Calculate an array of frequencies of oscillating signal using window
    """
    fs = []
    start = 0
    stop = window_width
    if stop > len(x):
        return fs
    while True:
        f = freq_stupid(x[start : stop], dt)
        fs.append(f)
        start += window_step
        stop += window_step
        if stop > len(x):
            break
    return np.array(fs)
