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

"""Functions for modulation and demodulation."""

from math import pi, cos, isnan
import numpy as np
from numpy import unwrap, angle, diff
import scipy.signal as sig


def harm(length, sample_rate, amp, freq, phi=0,
         noise_a=None, noise_f=None):
    """Generate harmonic signal.

    Parameters
    ----------
    length: float
        Length pf signal (sec).
    sample_rate: float
        Sampling frequency (Hz).
    amp: float
        Amplitude of signal.
    freq: Object
        Frequency of signal (Hz).
    phi: float
        Initial phase (radians).
    noise_a: callable
        Returns noise value added to amplitude.
    noise_f: callable
        Returns noise value added to frequency.

    Returns
    -------
    : np.array
        Signal values.
    : np.array
        Time values.
    """
    ts = np.arange(0, length, 1 / sample_rate)

    xs = []
    for t in ts:
        x = _ns(amp, noise_a) * cos(_ns(2*pi*freq*t + phi, noise_f))
        xs.append(x)

    return np.array(xs), ts


def amp_mod(length, sample_rate, func, freq, phi=0,
            noise_f=None, noise_a=None):
    """Amplitude modulation.

    Parameters
    ----------
    length: float
        Length pf signal (sec).
    sample_rate: float
        Sampling frequency (Hz).
    freq: float
        Frequency of signal (Hz).
    phi: float
        Initial phase (radians).
    func: Object
        Function that returns amplitude value depending on time.
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    : np.array
        Signal values.
    : np.array
        Time values.
    """
    ts = np.arange(0, length, 1/sample_rate)

    full_phase = phi
    delta_ph = 2*pi*freq / sample_rate
    xs = []
    for t in ts:
        x = _ns(func(t) * cos(_ns(full_phase, noise_f)), noise_a)
        xs.append(x)
        full_phase += delta_ph

    return np.array(xs), ts


def freq_mod(length, sample_rate, amp, func, phi=0,
             noise_f=None, noise_a=None):
    """Amplitude modulation.

    Parameters
    ----------
    length: float
        Length pf signal (sec).
    sample_rate: float
        Sampling frequency (Hz).
    amp: float
        Amplitude of signal.
    phi: float
        Initial phase (radians).
    func: Object
        Function that returns frequency values (in Hz) depending on
        time.
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    : np.array
        Signal values.
    : np.array
        Full phase values.
    : np.array
        Time values.
    """

    ts = np.arange(0, length, 1/sample_rate)

    full_phase = phi
    xs, phs = [], []
    for t in ts:
        x = _ns(amp * cos(_ns(full_phase, noise_f)), noise_a)
        xs.append(x)
        phs.append(full_phase)
        full_phase += 2*pi*func(t) / sample_rate

    return np.array(xs), np.array(phs), ts


def phase_mod(length, sample_rate, amp, freq, func,
              noise_f=None, noise_a=None):
    """Phase modulation.

    Parameters
    ----------
    length: float
        Length pf signal (sec).
    sample_rate: float
        Sampling frequency (Hz).
    amp: float
        Amplitude of signal.
    freq: float
        Frequency of signal (Hz).
    func: Object
        Function that returns phase values (in radians) depending on
        time.
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    : np.array
        Signal values.
    : np.array
        Time values.
    """
    ts = np.arange(0, length, 1/sample_rate)
    xs = []
    for t in ts:
        arg = _ns(2*pi*freq*t + func(t), noise_f)
        x = _ns(amp * cos(arg), noise_a)
        xs.append(x)

    return np.array(xs), ts


def _ns(x, func=None):
    if func:
        return x + func()
    return x


def freq_amp_mod(length, sample_rate, a_func, f_func, phi=0):
    """Simultaneous frequency and amplitude modulation.

    Parameters
    ----------
    length: float
        Length pf signal (sec).
    sample_rate: float
        Sampling frequency (Hz).
    a_func: Object
        Function that returns amplitude value depending on time.
    f_func: Object
        Function that returns frequency values (in Hz) depending on
        time.
    phi: float
        Initial phase (radians).

    Returns
    -------
    : np.array
        Signal values.
    : np.array
        Full phase values.
    : np.array
        Time values.
    """
    ts = np.arange(0, length, 1/sample_rate)

    full_phase = phi
    xs = []
    phs = []
    for t in ts:
        xs.append(a_func(t) * cos(full_phase))
        phs.append(full_phase)
        full_phase += 2*pi * f_func(t) / sample_rate

    return np.array(xs), np.array(phs), ts


def iq_demod(xdata, tdata, f_central, a_coeffs, b_coeffs):
    """Return instantaneous frequency of modulated signal using IQ
    processing.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    tdata: array_like
        Time values.
    f_central: float
        Carrier frequency.
    a_coeffs: array_like
        a values of filter.
    b_coeffs: array_like
        b values of filter.

    Returns
    -------
    : np.ndarray of floats
        Instantaneous frequency values.
    : np.ndarray
        Time values.
    """
    muli = xdata * np.cos(2*pi * f_central * tdata)
    mulq = xdata * np.sin(2*pi * f_central * tdata)
    muli_low = sig.lfilter(b_coeffs, a_coeffs, muli)
    mulq_low = sig.lfilter(b_coeffs, a_coeffs, mulq)
    analytic = muli_low + 1j * mulq_low
    phase = -unwrap(angle(analytic))
    freq = diff(phase) / 2 / pi / (tdata[1] - tdata[0]) + f_central
    return freq, tdata[:-1]


def envelope_by_extremums(xdata, sample_rate=1, tdata=None):
    """Calculate envelope by local extremums of signals.

    Parameters
    ----------
    xdata: array_like
        Signal values.
    sample_rate: float
        Sampling frequency.
    tdata: array_like
        Time values. Use it for unregular discretized input signal.

    Returns
    --------
    : np.array
        Damping values.
    : np.array
        Time values.
    """
    if tdata is None:
        tdata = np.linspace(0, (len(xdata)-1)/sample_rate, len(xdata))
    t_new = []
    x_new = []
    xabs = abs(xdata)
    for x_l, x_c, x_r, t_c in zip(xabs[:-2], xabs[1:-1],
                                  xabs[2:], tdata[1:-1]):
        if (x_l < x_c) and (x_c >= x_r):
            t_new.append(t_c)
            x_new.append(x_c)
    if xabs[-1] > xabs[-2]:
        t_new.append(tdata[-1])
        x_new.append(xabs[-1])
    return np.array(x_new), np.array(t_new)


def digital_hilbert_filter(ntaps=101, window='hamming'):
    """Calculate digital hilbert filter.

    Parameters
    ----------
    ntaps: integer
        Length of filter.
    window: str
        Window. Default is 'hamming'.

    Returns
    -------
    : np.array
        Filter.
    """
    if ntaps % 2 == 0:
        raise ValueError("ntaps of digital Hilbert filter must be odd.")

    coeffs = np.zeros(ntaps)
    num = ntaps // 2
    for k in range(1, num+1, 2):
        coeffs[num + k] = 2 / pi / k
        coeffs[num - k] = -2 / pi / k

    wind = sig.get_window(window, ntaps)
    coeffs *= wind
    return coeffs


def freq_by_extremums(xdata, sample_rate):
    """Calculate frequency of oscillating signal by extremums.

    Parameters
    ----------
    xdata: array_like
        Values of input signals.
    sample_rate: float
        Sampling frequency (Hz).

    Returns
    -------
    : float
        Frequency.
    """

    if len(xdata) < 3:
        raise ValueError("Short signal")

    T = len(xdata) / sample_rate

    max_total = 0
    min_total = 0
    for prev, curr, nxt in zip(xdata[:-2], xdata[1:-1], xdata[2:]):
        if (prev < curr) and (curr >= nxt):
            max_total += 1
        if (prev > curr) and (curr <= nxt):
            min_total += 1

    if xdata[0] > xdata[1]:
        max_total += 1

    if xdata[0] < xdata[1]:
        min_total += 1

    return (max_total + min_total) / 2 / T


def freq_by_zeros(xdata, sample_rate):
    """Calculate average frequency of detrended oscillating signal by
    counting zeros."""

    T = len(xdata) / sample_rate

    zeros_total = 0
    for prev, curr in zip(xdata[:-1], xdata[1:]):
        if prev * curr < 0:
            zeros_total += 1
        elif prev != 0 and curr == 0:
            zeros_total += 1

    return zeros_total / 2 / T


def linint(xdata, tdata, ts_new):
    """Find values of xdata in ts_new points.

    Parameters
    ----------
    xdata: np.ndarray
        Signal values.
    tdata: np.ndarray
        Time values.
    ts_new: np.ndarray
        New time values.

    Returns
    -------
    : np.ndarray
        New signal values.
    """
    x_new = np.zeros(len(ts_new)) * np.nan
    for x_p, t_p, x_c, t_c in zip(xdata[:-1], tdata[:-1],
                                  xdata[1:], tdata[1:]):
        k = (x_c - x_p) / (t_c - t_p)
        b = x_p - k*t_p
        ind = (ts_new >= t_p) & (ts_new <= t_c)
        x_new[ind] = k * ts_new[ind] + b
    return x_new


def wave_lens(xdata, tdata):
    """Calculate wave lengths of signal by space between zeros.

    Parameters
    ----------
    xdata: np.ndarray
        Signal values.
    tdata: np.ndarray
        Time values.

    Returns
    -------
    : np.ndarray
        Wave lengths.
    : np.ndarray
        Time values.
    """
    tms = []
    for t_c, x_p, x_c in zip(tdata[1:], xdata[:-1], xdata[1:]):
        if x_p * x_c < 0:
            tms.append(t_c)
    lens = np.diff(tms) * 2
    t_lens = np.array(tms[1:])
    return lens, t_lens


def freqs_by_wave_len(xdata, tdata, cut_nans=True):
    """Calculate frequencies using lenghs of waves and linear
    interpolation.

    Parameters
    ----------
    xdata: np.ndarray
        Signal values.
    tdata: np.ndarray
        Time values.
    cut_nans: boolean
        If True, the nan values at the ends of the of the produced
        array will removed.

    Returns
    -------
    : np.ndarray
        Freqs values.
    """
    wls, t_wl = wave_lens(xdata, tdata)
    freqs = 1 / linint(wls, t_wl, tdata)
    if cut_nans:
        freqs_cut = []
        t_cut = []
        for (f, tt) in zip(freqs, tdata):
            if f is not None and not isnan(f):
                freqs_cut.append(f)
                t_cut.append(tt)
        return np.array(freqs_cut), t_cut
    return freqs
