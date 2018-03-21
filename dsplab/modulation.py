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

def am(T, fs, f, phi, func):
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
        Function that returns amplitude values depending on time.

    Returns
    -------
    xs: np.array
        Signal values.
    ts: np.array
        Time values.

    """
    ph = phi
    t = 0
    delta_t = 1.0/fs
    delta_ph = 2 * np.pi / fs
    N = int(T*fs) 
    xs = []
    ts = []
    for i in range(N):
        A = func(t)
        x = A*np.cos(ph)
        xs.append(x)
        ts.append(t)
        t += delta_t
        ph += delta_ph
    xs = np.array(xs)
    ts = np.array(ts)
    return xs, ts
    
def fm(T, fs, a, phi, func):
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

    Returns
    -------
    xs: np.array
        Signal values.
    ts: np.array
        Time values.

    """
    ph = phi
    t = 0
    delta_t = 1.0/fs
    N = int(T*fs) 
    xs = []
    ts = []
    for i in range(N):
        x = a*np.cos(ph)
        xs.append(x)
        ts.append(t)
        t += delta_t
        delta_ph = 2*np.pi*func(t)/fs
        ph += delta_ph
    xs = np.array(xs)
    ts = np.array(ts)
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
