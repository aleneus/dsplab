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

def spectrum(x, fs, window='hamming', one_side=False, return_amplitude=True, extra_len=None):
    """
    Return the Fourier spectrum of signal.

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency (Hz)
    window : str
        Window.
    one_side : boolean
        If True, the one-side spectrum is calculated (default value is False)
    return_amplitude : boolean
        If True, the amplitude spectrum is calculated

    Returns
    -------
    X : np.array of complex numbers
        Spectrum
    f_X : np.array of floats
        Frequency values (Hz)

    """
    # window signal
    win = sig.get_window(window, len(x))
    xx = x * win * len(win)/sum(win)
    # FFT
    if extra_len:
        n = max(extra_len, len(x))
    else:
        n = len(x)
    X = 2 * fftpack.fft(xx, n) / len(x)
    f_X = np.fft.fftfreq(len(X), 1/fs)
    # one-side
    if one_side:
        ind = f_X>=0
        f_X = f_X[ind]
        X = X[ind]
    # calc amplitude
    if return_amplitude:
        X = abs(X)
    return X, f_X

def stft(x, fs, nseg, nstep, window='hamming', nfft=None, padded=False):
    """
    Return result of short-time fourier transform.

    Parameters
    ----------
    x : numpy.ndarray
        Signal.
    fs : float 
       Sampling frequency (Hz).
    nseg : int
        Length of segment (in samples).
    nstep : int
        Length of step (in samples).
    window : str
        Window.
    nfft : int 
        Length of the FFT. If None or less than nseg, the FFT length is nseg.

    Returns
    -------

    Xs : numpy.ndarray
        Result of STFT.
    
    """
    Xs=[]
    # TODO: consider nstep in padding
    if padded:
        L = len(x) + (nseg - len(x) % nseg) % nseg
        z = np.zeros(L)
        z[:len(x)] = x.copy()
        xx = z

    for i in range(0, len(xx)-nseg + 1, nstep):
        seg = xx[i : i+nseg]
        X, f_X = spectrum(seg, fs, extra_len=nfft, window=window)
        Xs.append(X)
    return np.array(Xs)

def calc_specgram(x, fs=1, t=[], nseg=256, nstep=None, freq_bounds=None, extra_len=1000):
    """
    Return spectrogram data prepared to further plotting.

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency (Hz)
    t : array_like
        Time values (sec)
    nseg : integer
        Length of window (number of samples)
    nstep : integer
        Length of step between Fourier transforms
    freq_bounds : tuple of 2 float
        Bounds of showed band
    extra_len : integer
        Number of values using for fft

    Return
    ------
    Xs : np.ndarray
        Array of spectrums
    t_new : np.ndarray
        Time values

    """
    if len(t)==0:
        t = np.linspace(0, (len(x)-1)*fs, len(x))
    else:
        fs = 1/(t[1] - t[0])
    if not nstep:
        nstep = nseg//2
    Xs = 2*stft(x=x, fs=fs, nseg=nseg, nstep=nstep, nfft=extra_len, padded=True)
    if freq_bounds:
        freqs = np.fft.fftfreq(len(Xs[0]), 1/fs)
        ind = (freqs>=freq_bounds[0])&(freqs<=freq_bounds[1]) # TODO: thick about it, maybe mistake here
        Xs = Xs[:,ind]
    t_new = np.linspace(t[nseg], t[-1], len(Xs))
    return np.transpose(Xs), t_new
