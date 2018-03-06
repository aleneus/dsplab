# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNUGeneral Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import numpy.linalg as linalg

def prony_decomp(x, L):
    """ 
    Prony decomposition of signal.

    Parameters
    ----------
    x : array_like
        Signal values
    L : integer
        Number of components. 2*L must be less tham length of x
    
    Returns
    -------
    ms : np.array
        Mu-values
    cs : np.array
        C-values
    es : np.array
        Components

    """
    N = len(x)
    if 2*L > N:
        return None
    d = np.array([x[i] for i in range(L, N)])
    D = []
    for i in range(L, N):
        D_row = []
        for j in range(0, L):
            D_row.append(x[i-j-1])
        D.append(np.array(D_row))
    D = np.array(D)
    a = linalg.lstsq(D, d)[0] # TODO: think here if mistake

    p = np.array([1] +[-ai for ai in a])
    ms = np.roots(p)

    d = np.array([x[i] for i in range(0, N)])
    D = []
    for i in range(0, N):
        D_row = []
        for j in range(0, L):
            D_row.append(ms[j]**i)
        D.append(np.array(D_row))
    D = np.array(D)

    cs = linalg.lstsq(D, d)[0] # TODO: think here if mistake

    es = []
    for i in range(0, L):
        e = [cs[i]*(ms[i]**k) for k in range(0, N)]
        es.append(np.array(e).real)
    es = np.array(es)

    return ms, cs, es
