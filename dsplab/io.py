# Copyright (C) 2017-2018 Aleksandr Popov

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

def read_signal_from_csv(file_name, t_column=0, x_column=1, start_line=1, fs=None, delimiter=';'):
    """ Deprecated. """
    print("Warning! dsplab.io.read_signal_from_csv is deprecated.")
    data = np.genfromtxt(file_name, delimiter=delimiter)
    data = data.transpose()
    x = np.array(data[x_column][start_line:])
    if not fs:
        t = np.array(data[t_column][start_line:])
    else:
        t = np.linspace(0, (len(x)-1)/fs, len(x))
    return x, t
