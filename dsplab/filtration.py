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

""" Filtration of signals. """

import numpy as np
import scipy.signal as sig
from scipy.fftpack import fft, ifft


def _stupid_filter(xdata, fr_resp):
    """ Filter signal using setted frequency response.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    fr_resp: np.array
        Frequency response of ideal filter.

    Returns
    -------
    : np.array
        Filteres signal.
    """
    spectrum = fft(xdata * sig.tukey(len(xdata)))
    res_xs = np.real(ifft(spectrum * fr_resp))
    return res_xs


def stupid_lowpass_filter(xdata, sample_rate, cutoff):
    """ Return low-pass filtered signal.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    sample_rate: float
        Sampling frequency.
    cutoff: float
        Cutoff frequency.

    Returns
    -------
    : np.array
        Filteres signal.
    """
    num = len(xdata)
    fr_resp = np.zeros(num)
    freqs = np.fft.fftfreq(num, 1/sample_rate)
    fr_resp[abs(freqs) <= cutoff] = 1
    res_xs = _stupid_filter(xdata, fr_resp)
    return res_xs


def stupid_bandpass_filter(xdata, sample_rate, bandpass):
    """ Return low-pass filtered signal.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    sample_rate: float
        Sampling frequency.
    bandpass: np.array of 2 floats
        Bounds of bandpass (Hz).

    Returns
    -------
    : np.array
        Filteres signal.
    """
    num = len(xdata)
    fr_resp = np.zeros(num)
    freqs = np.fft.fftfreq(num, 1 / sample_rate)
    fr_resp[(abs(freqs) >= bandpass[0]) & (abs(freqs) <= bandpass[1])] = 1
    res_xs = _stupid_filter(xdata, fr_resp)
    return res_xs


def butter_filter(xdata, sample_rate, freqs, order, btype='band'):
    """ Butterworth filter.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    sample_rate: float
        Sampling frequency (Hz).
    freqs: array_like
        One or two frequencies.
    order: integer
        Order of filter.
    btype: str ('band' | 'lowpass')
        Type of filter.

    Returns
    -------
    : np.array
        filtered signal.
    """
    nyq = 0.5 * sample_rate
    freqs = np.array(freqs)
    freqs /= nyq
    b_coeffs, a_coeffs = sig.butter(order, freqs, btype=btype)
    res_xs = sig.lfilter(b_coeffs, a_coeffs, xdata)
    return res_xs


def find_butt_bandpass_order(band, sample_rate):
    """ Claculate the order of Butterworth bandpass filter using
    minimization of metric between ideal and real frequency response.

    Parameters
    ----------
    band: array_like
        Pair of frequencies. Bounds of bandpass (Hz).
    sample_rate: float
        Sample rate (Hz).

    Returns
    -------
    : integer
        Order of filter.
    """
    spectrum_len = round(60 * 120 * sample_rate)
    unit_pulse = np.zeros(spectrum_len)
    unit_pulse[1] = 1
    ideal_fr = np.zeros(spectrum_len)
    freqs = np.fft.fftfreq(spectrum_len, 1/sample_rate)
    ideal_fr[(freqs >= band[0]) & (freqs <= band[1])] = 1
    ideal_fr = ideal_fr[:spectrum_len//2]
    prev_metric = np.inf
    for order in range(3, 21):
        impulse_response = butter_filter(
            unit_pulse,
            sample_rate,
            band,
            order,
            btype='band'
        )
        real_fr = abs(fft(impulse_response))[:spectrum_len//2]
        metric = np.sum((real_fr - ideal_fr)**2)**0.5
        best_order = order
        if (np.isnan(metric)) or (metric >= prev_metric):
            best_order -= 1
            break
        prev_metric = metric
    return best_order-1


def haar_one_step(xdata, tdata, denominator=2):
    """ One cascade of Haar transform.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    tdata: array_like
        Time values.
    denominator: integer
        Denominator used in Haar transform (default is 2).

    Returns
    -------
    : np.array
        Scaled signal values.
    : np.array.
        Details of x
    : np.array.
        Decimated time values
    """
    scl = []
    det = []
    res_ts = []
    for x_left, x_right in zip(xdata[::2], xdata[1::2]):
        scl.append((x_left+x_right)/denominator)
        det.append((x_left-x_right)/denominator)
    res_ts = tdata[1::2]
    return np.array(scl), np.array(det), np.array(res_ts)


def haar_scaling(xdata, tdata, steps_number):
    """ Scaling with Haar transform.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    tdata: array_like
        Time values.
    steps_number: integer
        Number of cascades.

    Returns
    -------
    : np.array
        Scaled signal values.
    : np.array
        Decimated time values.
    """
    res_xs = xdata.copy()
    res_ts = tdata.copy()
    i = 0
    while i < steps_number:
        res = haar_one_step(res_xs, res_ts, denominator=2)
        res_xs, res_ts = res[0], res[2]
        i += 1
    return res_xs, res_ts


def smooth(xdata, ntaps=3, cut=True):
    """ Smooth signal with Hamming window. """
    wind = np.hamming(ntaps)
    wind = wind / sum(wind)
    res = sig.lfilter(wind, [1], xdata)
    if cut:
        res = res[ntaps:]
    return res


def trend_smooth(xdata, sample_rate=1, tdata=None, cut_off=0.5):
    """ Calculate trend of signal using smoothing filter.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    tdata: array_like
        Time values.
    cut_off: float
        The frequencies lower than this are trend's frequencies.

    Returns
    -------
    : np.array
        Trend values.
    : np.array
        Time values.
    """
    x_len = len(xdata)

    if tdata is None:
        tdata = np.linspace(0, (x_len-1)*sample_rate, x_len)
    else:
        sample_rate = 1.0 / (tdata[1] - tdata[0])

    win_len = int(sample_rate / 2 / cut_off)
    if win_len >= x_len:
        return None
    trend_xs = smooth(xdata, win_len)
    trend_ts = tdata[win_len:].copy()
    return trend_xs, trend_ts
