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

def freq_by_maxs(x, dt):
    T = len(x)*dt
    n = 0
    for x_prev, x_current, x_next in zip(x[:-2], x[1:-1], x[2:]):
        if (x_prev < x_current) and (x_current >= x_next):
            n += 1
    f = n / T
    return f

def freq_by_mins(x, dt):
    T = len(x)*dt
    n = 0
    for x_prev, x_current, x_next in zip(x[:-2], x[1:-1], x[2:]):
        if (x_prev > x_current) and (x_current <= x_next):
            n += 1
    f = n / T
    return f

def freq_by_zeros(x, dt):
    T = len(x)*dt
    n = 0
    for x_prev, x_current in zip(x[:-1], x[1:]):
        if x_prev * x_current <= 0:
            n += 1
    f = n / T
    return f

def calc_freqs_stupid(x, dt, method = "max", window_width = 100, window_step = 50):
    fs = None
    return fs
