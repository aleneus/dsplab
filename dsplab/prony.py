# Copyright (C) 2017-2022 Aleksandr Popov
# Copyright (C) 2021-2022 Kirill Butin

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
from numpy import linalg


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

    f_mat = []
    for i in range(ncomp, samples_total):
        row = [xdata[i-j-1] for j in range(0, ncomp)]
        f_mat.append(row)
    f_col = xdata[ncomp:]

    f_sols = linalg.lstsq(f_mat, f_col, rcond=None)[0]
    mu_vals = np.roots([1] + list(-f_sols))

    d_mat = []
    for i in range(samples_total):
        row = [mu_vals[j]**i for j in range(ncomp)]
        d_mat.append(np.array(row))

    c_vals = linalg.lstsq(d_mat, xdata, rcond=None)[0]

    comps = []
    for i in range(0, ncomp):
        comp = [c_vals[i] * (mu_vals[i]**k) for k in range(samples_total)]
        comps.append(np.array(comp).real)

    return mu_vals, c_vals, np.array(comps)
