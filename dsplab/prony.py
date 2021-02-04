# Copyright (C) 2017-2021 Aleksandr Popov
# Copyright (C) 2021 Kirill Butin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module implements Prony decomposition of signal."""

import numpy as np
import numpy.linalg as linalg


def prony_decomp(xdata, ncomp):
    """Prony decomposition of signal.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    ncomp: integer
        Number of components. 2*ncomp must be less tham length of xdata.

    Returns
    -------
    : np.array
        Mu-values.
    : np.array
        C-values.
    : np.array
        Components.
    """
    samples_total = len(xdata)
    if 2*ncomp > samples_total:
        return None
    d_matrix = []
    for i in range(ncomp, samples_total):
        row = [xdata[i-j-1] for j in range(0, ncomp)]
        d_matrix.append(np.array(row))
    d_matrix = np.array(d_matrix)
    d_column = np.array([xdata[i] for i in range(ncomp, samples_total)])

    a = linalg.lstsq(d_matrix, d_column, rcond=None)[0]
    p = np.array([1] + [-ai for ai in a])
    mu_vals = np.roots(p)

    d_matrix = []
    for i in range(samples_total):
        row = [mu_vals[j]**i for j in range(ncomp)]
        d_matrix.append(np.array(row))
    d_matrix = np.array(d_matrix)
    d_column = np.array([xdata[i] for i in range(samples_total)])

    c_vals = linalg.lstsq(d_matrix, d_column, rcond=None)[0]

    components = []
    for i in range(0, ncomp):
        comp = [c_vals[i] * (mu_vals[i]**k) for k in range(samples_total)]
        components.append(np.array(comp).real)
    components = np.array(components)

    return mu_vals, c_vals, components
