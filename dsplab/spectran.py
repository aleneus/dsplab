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

"""Some functions for spectral analysis."""

import numpy as np
import scipy.fftpack as fftpack
import scipy.signal as sig


def spectrum(xdata, sample_rate=1, window='hamming', one_side=False,
             return_amplitude=True, extra_len=None, save_energy=False):
    """Return the Fourier spectrum of signal.

    Parameters
    ----------
    xdata: array_like
        Signal values
    sample_rate: float
        Sampling frequency (Hz)
    window: str
        Window.
    one_side: boolean
        If True, the one-side spectrum is calculated (default value is
        False)
    return_amplitude: boolean
        If True, the amplitude spectrum is calculated
    extra_len: int
        If the value is set, the signal is padded with zeros to the
        extra_len value.
    save_energy: boolean
        If True, the result of FFT has the same energy as signal.  If
        False, the X (spectrum) is multiplied to 2/len(xdata). Use False
        if you want to see the correct amplitude of components in
        spectrum.

    Returns
    -------
    : np.ndarray of complex numbers
        Spectrum
    : np.ndarray of floats
        Frequency values (Hz)
    """
    win = sig.get_window(window, len(xdata))
    x_faded = xdata * win * len(win)/sum(win)

    actual_len = len(xdata)
    if extra_len:
        actual_len = max(extra_len, actual_len)

    sp_comp = fftpack.fft(x_faded, actual_len)
    if not save_energy:
        sp_comp *= 2/len(xdata)
    freqs = np.fft.fftfreq(len(sp_comp), 1/sample_rate)

    if one_side:
        ind = freqs >= 0
        freqs = freqs[ind]
        sp_comp = sp_comp[ind]

    if return_amplitude:
        return abs(sp_comp), freqs

    return sp_comp, freqs


def stft(xdata, sample_rate=1, nseg=256,
         nstep=None, window='hamming', nfft=None, padded=False):
    """Return result of short-time fourier transform.

    Parameters
    ----------
    xdata: numpy.ndarray
        Signal.
    sample_rate: float
       Sampling frequency (Hz).
    nseg: int
        Length of segment (in samples).
    nstep: int
        Optional. Length of step (in samples). If not setted then
        equal to nseg//2.
    window: str
        Window.
    nfft: int
        Length of the FFT. If None or less than nseg, the FFT length
        is nseg.

    Returns
    -------
    : numpy.ndarray
        Result of STFT, two-side spectrums.
    """
    if not nstep:
        nstep = nseg//2
    x_copy = xdata.copy()
    if padded:
        actual_len = len(x_copy) + (nseg - len(x_copy) % nseg) % nseg
        zer = np.zeros(actual_len)
        zer[:len(x_copy)] = x_copy
        x_copy = zer

    specs = []
    for i in range(0, len(x_copy)-nseg + 1, nstep):
        seg = x_copy[i: i+nseg]
        spec = spectrum(seg, sample_rate,
                        extra_len=nfft, window=window, save_energy=True)[0]
        specs.append(spec)

    return np.array(specs)


def calc_specgram(xdata, sample_rate=1, tdata=None, nseg=256,
                  nstep=None, freq_bounds=None, extra_len=None):
    """Return spectrogram data prepared to further plotting.

    Parameters
    ----------
    xdata: array_like
        Signal values
    sample_rate: float
        Sampling frequency (Hz)
    tdata: array_like
        Time values (sec)
    nseg: integer
        Length of window (number of samples)
    nstep: integer
        Length of step between Fourier transforms
    freq_bounds: tuple of 2 float
        Bounds of showed band
    extra_len: integer
        Number of values using for fft

    Return
    ------
    : np.ndarray
        Array of spectrums
    : np.ndarray
        Time values
    """
    if len(xdata) < nseg:
        return [], []
    if tdata is None:
        tdata = np.linspace(0, (len(xdata)-1)*sample_rate, len(xdata))
    else:
        sample_rate = 1/(tdata[1] - tdata[0])
    if not nstep:
        nstep = nseg//2
    specs = 2*stft(xdata=xdata, sample_rate=sample_rate, nseg=nseg,
                   nstep=nstep, nfft=extra_len, padded=True)
    if freq_bounds:
        freqs = np.fft.fftfreq(len(specs[0]), 1/sample_rate)
        ind = (freqs >= freq_bounds[0]) & (freqs <= freq_bounds[1])
        specs = specs[:, ind]
    t_new = np.linspace(tdata[nseg-1], tdata[-1], len(specs))
    return np.transpose(specs), t_new
