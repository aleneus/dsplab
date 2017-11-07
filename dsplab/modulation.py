# Copyright (C) 2017 Aleksandr Popov

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
from scipy.signal import firwin

def calc_freq_phasor(x, t, f_central, f_width, filter_order=5):
    """
    Return instantaneous frequency of modulated signal using phasor.

    Parameters
    ----------
    x : array_like
        Signal values
    t : array_like
        Time values
    f_central : float
        Central frequency (Hz)
    f_width : float
        Bandwidth
    filter_order : integer
        Order of filter

    Returns
    -------
    freqs : np.array
        Instantaneous frequency values

    """
    # TODO: need more universal filter tool
    fs = 1/(t[1] - t[0])
    yI = x * np.cos(2*np.pi*f_central*t)
    yQ = x * np.sin(2*np.pi*f_central*t)
    yI_ = flt.butter_filter(yI, fs, f_width/2, order=filter_order, btype='lowpass')
    yQ_ = flt.butter_filter(yQ, fs, f_width/2, order=filter_order, btype='lowpass')
    a = np.diff(yI_) * yQ_[:-1]
    b = np.diff(yQ_) * yI_[:-1]
    c = (yI_**2)[:-1]
    d = (yQ_**2)[:-1]
    freqs = (a - b) / (c + d)
    return freqs + f_central # TODO: return t?

# TODO: why calc_freq_phasor_fir is not in frequency module?
def calc_freq_phasor_fir(x, t, f_central, f_width, filter_len):
    """
    Return instantaneous frequency of modulated signal using phasor.

    Returns
    -------
    freqs : np.array
        Instantaneous frequency values

    """
    fs = 1/(t[1] - t[0])
    yI = x * np.cos(2*np.pi*f_central*t)
    yQ = x * np.sin(2*np.pi*f_central*t)
    h = firwin(filter_len, f_width/2, nyq=fs/2)
    yI_ = np.convolve(yI, h, mode="same")
    yQ_ = np.convolve(yQ, h, mode="same")
    a = np.diff(yI_) * yQ_[:-1]
    b = np.diff(yQ_) * yI_[:-1]
    c = (yI_**2)[:-1]
    d = (yQ_**2)[:-1]
    freqs = (a - b) / (c + d)
    return freqs + f_central # TODO: return t?
