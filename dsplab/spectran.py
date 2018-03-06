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

import scipy.fftpack as fftpack
import scipy.signal as sig
import numpy as np

# TODO: use calculated window, not string
# TODO: replace save_energy to some positive argument. Something like save_amplitude or fit_amplitude.
# TODO: Is the default value for save_energy correct?
def spectrum(x, fs=1, window='hamming', one_side=False, return_amplitude=True, extra_len=None, save_energy=False):
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
    save_energy : boolean
        If True, the result of FFT has the same energy as signal. 
        If False, the X (spectrum) is multiplied to 2/len(x). Use False if you want to see 
        the correct amplitude of components in spectrum.

    Returns
    -------
    X : np.ndarray of complex numbers
        Spectrum
    f_X : np.ndarray of floats
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
    #X = 2 * fftpack.fft(xx, n) / len(x)
    X = fftpack.fft(xx, n)
    if not save_energy:
        X *= 2/len(x)
    f_X = np.fft.fftfreq(len(X), 1/fs)
    # one-side
    if one_side:
        ind = f_X>=0
        f_X = f_X[ind]
        X = X[ind]
    # calc amplitude
    if return_amplitude: # TODO: result = 'amplitude|phase|None'
        X = abs(X)
    return X, f_X

# TODO: use calculates window, not string
# TODO: default values
def stft(x, fs=1, nseg=256, nstep=None, window='hamming', nfft=None, padded=False):
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
        Optional. Length of step (in samples). If not setted then equal to nseg//2.
    window : str
        Window.
    nfft : int 
        Length of the FFT. If None or less than nseg, the FFT length is nseg.

    Returns
    -------

    Xs : numpy.ndarray
        Result of STFT, two-side spectrums.
    
    """
    if not nstep:
        nstep = nseg//2 # TODO: test it
    # TODO: consider nstep in padding
    xx = x.copy()
    if padded:
        L = len(xx) + (nseg - len(xx) % nseg) % nseg
        z = np.zeros(L)
        z[:len(xx)] = xx
        xx = z

    Xs=[]
    for i in range(0, len(xx)-nseg + 1, nstep):
        seg = xx[i : i+nseg]
        X = spectrum(seg, fs, extra_len=nfft, window=window, save_energy=True)[0]
        Xs.append(X)
    return np.array(Xs) # TODO: return times too

# TODO: only here fs has default value
def calc_specgram(x, fs=1, t=[], nseg=256, nstep=None, freq_bounds=None, extra_len=None):
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
    if len(x) < nseg:
        return [], []
    if len(t)==0:
        t = np.linspace(0, (len(x)-1)*fs, len(x))
    else:
        fs = 1/(t[1] - t[0])
    if not nstep:
        nstep = nseg//2
    # TODO: test with None extra_len
    Xs = 2*stft(x=x, fs=fs, nseg=nseg, nstep=nstep, nfft=extra_len, padded=True)
    if freq_bounds:
        freqs = np.fft.fftfreq(len(Xs[0]), 1/fs)
        ind = (freqs>=freq_bounds[0])&(freqs<=freq_bounds[1]) # TODO: thick about it, maybe mistake here
        Xs = Xs[:,ind]
    t_new = np.linspace(t[nseg-1], t[-1], len(Xs))
    return np.transpose(Xs), t_new # TODO: consider mirroring when plotted
