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

import numpy as np
from numpy import pi, cos, sin, unwrap, angle, diff
import scipy.signal as sig


def harm(length, sample_rate, amp, freq, phi,
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
        arg = 2 * pi * freq * time_value + phi
        if noise_f is not None:
            arg += noise_f(time_value)
        values.append(amp_value * cos(arg))
    values = np.array(values)
    return values, times


def amp_mod(length, sample_rate, freq, phi, func,
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
    delta_ph = 2 * pi * freq / sample_rate
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


def freq_mod(length, sample_rate, amp, phi, func,
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
        delta_ph = 2 * pi * func(time_value) / sample_rate
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
        arg = 2 * pi * freq * time_value + func(time_value)
        if noise_f is not None:
            arg += noise_f(time_value)
        value = amp * cos(arg)
        if noise_a is not None:
            value += noise_a(time_value)
        values.append(value)
    values = np.array(values)
    return values, times


def freq_amp_mod(length, sample_rate, a_func, f_func, phi):
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
        delta_ph = 2 * pi * f_func(time_value) / sample_rate
        phs.append(full_phase)
        full_phase += delta_ph
    values = np.array(values)
    phs = np.array(phs)
    return values, phs, times


def iq_demod(values, times, f_central, a_coeffs, b_coeffs):
    """ Return instantaneous frequency of modulated signal using IQ processign.

    Parameters
    ----------
    values : array_like
        Signal values.
    times : array_like
        Time values.
    f_central : float
        Carrier frequency.
    a_coeffs : array_like
        a values of filter.
    b_coeffs : array_like
        b values of filter.

    Returns
    -------
    freq : np.ndarray of floats
        Instantaneous frequency values.
    t_freq : np.ndarray
        Time values.
    """
    muli = values * cos(2 * pi * f_central * times)
    mulq = values * sin(2 * pi * f_central * times)
    muli_low = sig.lfilter(b_coeffs, a_coeffs, muli)
    mulq_low = sig.lfilter(b_coeffs, a_coeffs, mulq)
    analytic = muli_low + 1j * mulq_low
    phase = -unwrap(angle(analytic))
    freq = diff(phase) / (2 * pi) / (times[1] - times[0]) + f_central
    return freq, times[:-1]
