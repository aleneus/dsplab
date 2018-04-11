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

def harmonic(T, fs, a, f, ph, noise_f=None, noise_a=None):
    """ Harmonic signal.

    Parameters
    ----------
    T: float
        Length pf signal (sec).
    fs: float
        Sampling frequency (Hz).
    a: float
        Amplitude of signal.
    f: Object
        Frequency of signal (Hz).
    ph: float
        Initial phase (radians).
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    xs: np.array
        Signal values.
    ts: np.array
        Time values.
    
    """
    ts = np.arange(0, T, 1/fs)
    xs = []
    for t in ts:
        amp = a
        if noise_a is not None:
            amp += noise_a(t)
        arg = 2*np.pi*f*t + ph
        if noise_f is not None:
            arg += noise_f(t)
        x = amp * np.cos(arg)
        xs.append(x)
    xs = np.array(xs)
    return xs, ts
    
def am(T, fs, f, phi, func, noise_f=None, noise_a=None):
    """ Amplitude modulation. 

    Parameters
    ----------
    T: float
        Length pf signal (sec).
    fs: float
        Sampling frequency (Hz).
    f: float
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
    xs: np.array
        Signal values.
    ts: np.array
        Time values.

    """
    ph = phi
    delta_ph = 2 * np.pi * f / fs
    dt = 1.0/fs
    ts = np.arange(0, T+dt, dt)
    xs = []
    for t in ts:
        A = func(t)
        if noise_f is None:
            x = A*np.cos(ph)
        else:
            x = A*np.cos(ph + noise_f(t))
        if noise_a is not None:
            x += noise_a(t)
        xs.append(x)
        ph += delta_ph
    xs = np.array(xs)
    return xs, ts
    
def fm(T, fs, a, phi, func, noise_f=None, noise_a=None):
    """ Amplitude modulation. 

    Parameters
    ----------
    T: float
        Length pf signal (sec).
    fs: float
        Sampling frequency (Hz).
    a: float
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
    xs: np.array
        Signal values.
    phs: np.array
        Full phase values.
    ts: np.array
        Time values.

    """
    ph = phi
    dt = 1.0/fs
    ts = np.arange(0, T+dt, dt)
    xs = []
    phs = []
    for t in ts:
        arg = ph
        if noise_f is not None:
            arg += noise_f(t)
        x = a*np.cos(arg)
        if noise_a is not None:
            x += noise_a(t)
        xs.append(x)
        phs.append(ph)
        delta_ph = 2*np.pi*func(t)/fs
        ph += delta_ph
    xs = np.array(xs)
    return xs, phs, ts

def phm(T, fs, a, f, func, noise_f=None, noise_a=None):
    """ Phase modulation. 

    Parameters
    ----------
    T: float
        Length pf signal (sec).
    fs: float
        Sampling frequency (Hz).
    a: float
        Amplitude of signal.
    f: float
        Frequency of signal (Hz).
    func: Object
        Function that returns phase values (in radians) depending on time.
    noise_f: Object
        Function that returns noise value added to frequency.
    noise_a: Object
        Function that returns noise value added to amplitude.

    Returns
    -------
    xs: np.array
        Signal values.
    ts: np.array
        Time values.

    """
    dt = 1.0/fs
    ts = np.arange(0, T+dt, dt)
    xs = []
    for t in ts:
        arg = 2*np.pi*f*t + func(t)
        if noise_f is not None:
            arg += noise_f(t)
        x = a*np.cos(arg)
        if noise_a is not None:
            x += noise_a(t)
        xs.append(x)
    xs = np.array(xs)
    return xs, ts

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
