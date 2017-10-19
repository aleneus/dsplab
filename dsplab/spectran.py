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

import scipy.fftpack as fftpack
import scipy.signal as sig
import numpy as np

def spectrum(x):
    """
    Return amplitude spectrum of signal.

    Parameters
    ----------
    x : array_like
        Signal.

    Returns
    -------
    X : numpy.array
        Two-side amplitude spectrum.

    """
    return abs(fftpack.fft(x))

def expand_to(x, new_len):
    """
    Add zeros to signal. For doing magick with resolution in spectrum.

    Parameters
    ----------
    x : array_like
        Signal values.
    new_len : integer
        New length.

    Returns
    -------
    x_exp : numpy.array
        Signal expanded by zeros.
    
    """
    if new_len <= len(x):
        return x
    x_exp = np.zeros(new_len)
    x_exp[0 : len(x)] = x
    return x_exp

def stft(x, dt, nseg, nstep, window='hanning', nfft=None, padded=False):
    """
    Return result of short-time fourier transform.

    Parameters
    ----------
    x : numpy.ndarray
        Signal.
    dt : float 
       Sampling period.
    window : str
        Type of window.
    nseg : int
        Length of segment (in samples).
    nstep : int
        Length of step (in samples).
    nfft : int 
        Length of the FFT. If None or less than nseg, the FFT length is nseg.

    Returns
    -------

    Xs : list of numpy.ndarray
        Result of STFT.
    
    """
    wind = sig.get_window(window, nseg)
    Xs=[]
    if padded:
        L = len(x) + (nseg - len(x) % nseg) % nseg
        x = expand_to(x, L)

    if not nfft:
        nseg_exp = nseg
    else:
        nseg_exp = max(nseg, nfft)
        
    for i in range(0, len(x)-nseg + 1, nstep):
        seg = x[i : i+nseg] * wind
        seg = expand_to(seg, nseg_exp)
        X = spectrum(seg)
        Xs.append(X)
    return Xs
