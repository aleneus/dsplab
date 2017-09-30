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

def freq_stupid(x, fs):
    """
    Calculate frequency of oscillating signal by extremums
    """
    T = len(x)/fs
    n_max = 0
    n_min = 0
    for x_prev, x_current, x_next in zip(x[:-2], x[1:-1], x[2:]):
        if (x_prev < x_current) and (x_current >= x_next):
            n_max += 1
        if (x_prev > x_current) and (x_current <= x_next):
            n_min += 1
    n = (n_max + n_min) / 2
    f = n / T
    return f

def freqs_stupid(x, fs, window_width = 1024, window_step = 512):
    """
    Calculate an array of frequencies of oscillating signal using window
    """
    freqs = []
    start = 0
    stop = window_width
    if stop > len(x):
        return freqs
    while True:
        f = freq_stupid(x[start : stop], fs)
        freqs.append(f)
        start += window_step
        stop += window_step
        if stop > len(x):
            break
    return np.array(freqs)
