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

""" Functions for modulation and demodulation. """

from math import pi, cos, sin
import numpy as np
from numpy import unwrap, angle, diff
import scipy.signal as sig


PI = pi
PI2 = 2 * PI


def harm(length, sample_rate, amp, freq, phi=0,
         noise_f=None, noise_a=None):
    """ Harmonic signal.

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
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    values: np.array
        Signal values.
    times: np.array
        Time values.
    """
    times = np.arange(0, length, 1 / sample_rate)
    values = []
    for time_value in times:
        amp_value = amp
        if noise_a is not None:
            amp_value += noise_a(time_value)
        arg = PI2 * freq * time_value + phi
        if noise_f is not None:
            arg += noise_f(time_value)
        values.append(amp_value * cos(arg))
    values = np.array(values)
    return values, times


def amp_mod(length, sample_rate, func, freq, phi=0,
            noise_f=None, noise_a=None):
    """ Amplitude modulation.

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
    values: np.array
        Signal values.
    times: np.array
        Time values.
    """
    full_phase = phi
    delta_ph = PI2 * freq / sample_rate
    sampling_period = 1.0 / sample_rate
    times = np.arange(0, length + sampling_period, sampling_period)
    values = []
    for time_value in times:
        if noise_f is None:
            value = func(time_value) * cos(full_phase)
        else:
            value = func(time_value) * cos(full_phase + noise_f(time_value))
        if noise_a is not None:
            value += noise_a(time_value)
        values.append(value)
        full_phase += delta_ph
    values = np.array(values)
    return values, times


def freq_mod(length, sample_rate, amp, func, phi=0,
             noise_f=None, noise_a=None):
    """ Amplitude modulation.

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
        Function that returns frequency values (in Hz) depending on time.
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    values: np.array
        Signal values.
    phs: np.array
        Full phase values.
    times: np.array
        Time values.
    """
    full_phase = phi
    times = np.arange(0, length + 1.0 / sample_rate, 1.0 / sample_rate)
    values = []
    phs = []
    for time_value in times:
        arg = full_phase
        if noise_f is not None:
            arg += noise_f(time_value)
        value = amp * cos(arg)
        if noise_a is not None:
            value += noise_a(time_value)
        values.append(value)
        phs.append(full_phase)
        delta_ph = PI2 * func(time_value) / sample_rate
        full_phase += delta_ph
    values = np.array(values)
    phs = np.array(phs)
    return values, phs, times


def phase_mod(length, sample_rate, amp, freq, func,
              noise_f=None, noise_a=None):
    """ Phase modulation.

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
        Function that returns phase values (in radians) depending on time.
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    values: np.array
        Signal values.
    times: np.array
        Time values.
    """
    sampling_period = 1.0 / sample_rate
    times = np.arange(0, length + sampling_period, sampling_period)
    values = []
    for time_value in times:
        arg = PI2 * freq * time_value + func(time_value)
        if noise_f is not None:
            arg += noise_f(time_value)
        value = amp * cos(arg)
        if noise_a is not None:
            value += noise_a(time_value)
        values.append(value)
    values = np.array(values)
    return values, times


def freq_amp_mod(length, sample_rate, a_func, f_func, phi=0):
    """ Simultaneous frequency and amplitude modulation.

    Parameters
    ----------
    length: float
        Length pf signal (sec).
    sample_rate: float
        Sampling frequency (Hz).
    a_func: Object
        Function that returns amplitude value depending on time.
    f_func: Object
        Function that returns frequency values (in Hz) depending on time.
    phi: float
        Initial phase (radians).

    Returns
    -------
    values: np.array
        Signal values.
    phs: np.array
        Full phase values.
    times: np.array
        Time values.
    """
    full_phase = phi
    sampling_period = 1.0 / sample_rate
    times = np.arange(0, length + sampling_period, sampling_period)
    values = []
    phs = []
    for time_value in times:
        arg = full_phase
        values.append(a_func(time_value) * cos(arg))
        delta_ph = PI2 * f_func(time_value) / sample_rate
        phs.append(full_phase)
        full_phase += delta_ph
    values = np.array(values)
    phs = np.array(phs)
    return values, phs, times


def iq_demod(values, times, f_central, a_coeffs, b_coeffs):
    """ Return instantaneous frequency of modulated signal using IQ processign.

    Parameters
    ----------
    values: array_like
        Signal values.
    times: array_like
        Time values.
    f_central: float
        Carrier frequency.
    a_coeffs: array_like
        a values of filter.
    b_coeffs: array_like
        b values of filter.

    Returns
    -------
    freq: np.ndarray of floats
        Instantaneous frequency values.
    t_freq: np.ndarray
        Time values.
    """
    muli = values * cos(PI2 * f_central * times)
    mulq = values * sin(PI2 * f_central * times)
    muli_low = sig.lfilter(b_coeffs, a_coeffs, muli)
    mulq_low = sig.lfilter(b_coeffs, a_coeffs, mulq)
    analytic = muli_low + 1j * mulq_low
    phase = -unwrap(angle(analytic))
    freq = diff(phase) / PI2 / (times[1] - times[0]) + f_central
    return freq, times[:-1]


def envelope_by_extremums(values, sample_rate=1, times=None):
    """ Calculate envelope by local extremums of signals.

    Parameters
    ----------
    values: array_like
        Signal values.
    sample_rate: float
        Sampling frequency.
    times: array_like
        Time values. Use it for unregular discretized input signal.

    Returns
    --------
    : np.array
        Damping values.
    : np.array
        Time values.
    """
    if times is None:
        times = np.linspace(0, (len(values)-1)/sample_rate, len(values))
    t_new = []
    x_new = []
    xabs = abs(values)
    for x_l, x_c, x_r, t_c in zip(xabs[:-2], xabs[1:-1],
                                  xabs[2:], times[1:-1]):
        if (x_l < x_c) and (x_c >= x_r):
            t_new.append(t_c)
            x_new.append(x_c)
    if xabs[-1] > xabs[-2]:
        t_new.append(times[-1])
        x_new.append(xabs[-1])
    return np.array(x_new), np.array(t_new)


def digital_hilbert_filter(ntaps=101, window='hamming'):
    """ Calculate digital hilbert filter.

    Parameters
    ----------
    ntaps: integer
        Length of filter.
    window: str
        Window. Default is 'hamming'.

    Returns
    -------
    coeffs: np.array
        Filter.
    """
    if ntaps % 2 == 0:
        raise ValueError("ntaps of digital Hilbert filter must be odd.")
    num = ntaps // 2
    coeffs = [1/PI/k * (1 - cos(PI * k)) for k in range(-num, 0)]
    coeffs += [0]
    coeffs += [1/PI/k * (1 - cos(PI * k)) for k in range(1, num+1)]
    wind = sig.get_window(window, ntaps)
    coeffs *= wind
    return coeffs
