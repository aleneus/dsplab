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

from scipy.signal import butter, lfilter
import numpy as np

def butter_lowpass(cutoff, fs, order):
    """ 
    Calculate a and b coefficients for Butterworth lowpass filter

    Parameters
    ----------
    cutoff : float
        Cutoff frequency (Hz)
    fs : float
        Sampling frequency (Hz)
    order : integer
        Order of filter

    Returns
    -------
    b : np.array
        b-values
    a : np.array
        a-values

    """
    nyq = 0.5 * fs
    b, a = butter(order, cutoff/nyq, btype='low')
    return b, a

def butter_lowpass_filter(x, cutoff, fs, order):
    """ 
    Filter signal with Butterworth lowpass filter

    Parameters
    ----------
    x : array_like
        Signal values
    cutoff : float
        Cutoff frequency (Hz)
    fs : float
        Sampling frequency (Hz)
    order : integer
        Order of filter

    Returns
    -------
    x_new : np.array
        Values of filtered signal

    """
    b, a = butter_lowpass(cutoff, fs, order)
    return lfilter(b, a, x)

def butter_bandpass(lowcut, highcut, fs, order):
    """ 
    Calculate a and b coefficients for Butterworth bandpass filter

    Parameters
    ----------
    lowcut : float
        Low-cut frequency (Hz)
    highcut : float
        High-cut frequency (Hz)
    fs : float
        Sampling frequency (Hz)
    order : integer
        Order of filter

    Returns
    -------
    b : np.array
        b-values
    a : np.array
        a-values

    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(x, lowcut, highcut, fs, order):
    """ 
    Filter signal with Butterworth bandpass filter

    Parameters
    ----------
    x : array_like
        Signal values
    lowcut : float
        Low-cut frequency (Hz)
    highcut : float
        High-cut frequency (Hz)
    fs : float
        Sampling frequency (Hz)
    order : integer
        Order of filter

    Returns
    -------
    x_new : np.array
        Values of filtered signal

    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, x)

def haar_one_step(x, t, denominator=2):
    """ 
    One cascade of Haar transform.

    Parameters
    ----------
    x : array_like
        Signal values
    t : array_like
        Time values
    denominator : integer
        Denominator used in Haar transform (default is 2)

    Returns
    -------
    x_s : np.array
        Scaled signal values
    x_d : np.array
        Details of x
    t_new : np.array
        Decimated time values

    """
    # TODO: use t or fs in arguments
    x_s = []
    x_d = []
    t_new = []
    for x_left, x_right in zip(x[::2], x[1::2]):
        x_s.append((x_left+x_right)/denominator)
        x_d.append((x_left-x_right)/denominator)
    t_new = t[1::2]
    return np.array(x_s), np.array(x_d), np.array(t_new)

def haar_scaling(x, t, steps_number):
    """ 
    Scaling with Haar transform.

    Parameters
    ----------
    x : array_like
        Signal values
    t : array_like
        Time values
    steps_number : integer
        Number of cascades

    Returns
    -------
    x_s : np.array
        Scaled signal values
    t_new : np.array
        Decimated time values

    """
    # TODO: validation of steps_number
    x_s = x.copy()
    t_new = t.copy()
    for i in range(steps_number):
        x_s, x_d, t_new = haar_one_step(x_s, t_new, denominator=2)
    return x_s, t_new
