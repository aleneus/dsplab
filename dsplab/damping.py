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

def damping_triangles(x):
    """ Calculate damping using triangle approximation
    """
    ts = []
    ds = []
    for x_prev, x_current, x_next in zip(x[:-2], x[1:-1], x[2:]):
        if (x_prev < x_current) and (x_current >= x_next):
            ts.append(0)
            ds.append(0)
    return np.array(ts), np.array(ds)