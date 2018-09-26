# Copyright (C) 2017-2018 Aleksandr Popov

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

""" This module implements Prony decomposition of signal. """

import numpy as np
import numpy.linalg as linalg


def prony_decomp(xdata, ncomp):
    """ Prony decomposition of signal.

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
    N = len(xdata)
    if 2*ncomp > N:
        return None
    d = np.array([xdata[i] for i in range(ncomp, N)])
    D = []
    for i in range(ncomp, N):
        D_row = []
        for j in range(0, ncomp):
            D_row.append(xdata[i-j-1])
        D.append(np.array(D_row))
    D = np.array(D)
    a = linalg.lstsq(D, d)[0]

    p = np.array([1] + [-ai for ai in a])
    ms = np.roots(p)

    d = np.array([xdata[i] for i in range(0, N)])
    D = []
    for i in range(0, N):
        D_row = []
        for j in range(0, ncomp):
            D_row.append(ms[j]**i)
        D.append(np.array(D_row))
    D = np.array(D)

    cs = linalg.lstsq(D, d)[0]

    es = []
    for i in range(0, ncomp):
        e = [cs[i]*(ms[i]**k) for k in range(0, N)]
        es.append(np.array(e).real)
    es = np.array(es)

    return ms, cs, es
