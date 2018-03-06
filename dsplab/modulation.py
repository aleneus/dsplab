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
import dsplab.filtration as flt

# TODO: [3] add tests
# TODO: [1] allow use t or fs
# TODO: [1] rename f_central to fc (f carrier)
def iq_demod(x, t, f_central, a, b):
    """ Return instantaneous frequency of modulated signal using IQ processign. 

    Parameters
    ----------
    x : array_like
        Signal values.
    t : array_like
        Time values.
    f_central : float
        Carrier frequency.
    a : array_like
        a values of filter.
    b : array_like
        b values of filter.

    Returns
    -------
    freq : np.ndarray of floats
        Instantaneous frequency values.
    t_freq : np.ndarray
        Time values.

    """
    fs = 1/(t[1] - t[0])
    yI = x * np.cos(2*np.pi*f_central*t)
    yQ = x * np.sin(2*np.pi*f_central*t)
    # TODO: [3] next works only for FIR now, some kind of stub
    yI_ = np.convolve(yI, b, mode="same") # TODO: [3] use lfilter and a
    yQ_ = np.convolve(yQ, b, mode="same") # TODO: [3] use lfilter and a
    analytic = yI_ + 1j*yQ_
    phase = -np.unwrap(np.angle(analytic))
    freq = np.diff(phase) / (2*np.pi) * fs + f_central
    return freq, t[:-1]
