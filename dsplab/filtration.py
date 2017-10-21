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

import scipy.signal as sig
import scipy.fftpack as fftpack
import numpy as np

def _stupid_filter(x, fs, fr):
    """
    Filter signal using setted frequency response.

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency
    fs : np.array
        Frequency response of ideal filter

    Returns
    -------
    xf : np.array
        Filteres signal

    """
    _x = x * sig.tukey(len(x))
    X = fftpack.fft(_x)
    return np.real(fftpack.ifft(X * fr))

def stupid_lowpass_filter(x, fs, cutoff):
    """
    Return low-pass filtered signal.

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency
    cutoff : float
        Cutoff frequency

    Returns
    -------
    xf : np.array
        Filteres signal

    """
    fr = np.zeros(len(x))
    f = np.fft.fftfreq(len(x), 1/fs)
    ind = abs(f)<=cutoff
    fr[ind] = 1
    return  _stupid_filter(x, fs, fr)

def stupid_bandpass_filter(x, fs, bandpass):
    """
    Return low-pass filtered signal.

    Parameters
    ----------
    x : array_like
        Signal values
    fs : float
        Sampling frequency
    bandpass : np.array of 2 floats
        Bounds of bandpass (Hz)

    Returns
    -------
    xf : np.array
        Filteres signal

    """
    fr = np.zeros(len(x))
    f = np.fft.fftfreq(len(x), 1/fs)
    ind = (abs(f) >= bandpass[0])&(abs(f)<=bandpass[1])
    fr[ind] = 1
    return  _stupid_filter(x, fs, fr)

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
    b, a = sig.butter(order, cutoff/nyq, btype='low')
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
    return sig.lfilter(b, a, x)

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
    b, a = sig.butter(order, [low, high], btype='band')
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
    return sig.lfilter(b, a, x)

def find_butt_bandpass_order(band, fs):
    """
    Claculate the order of Butterworth bandpass filter using minimization of metric between ideal and real frequency response.

    Parameters
    ----------
    band : array_like
        Pair of frequencies. Bounds of bandpass (Hz)
    fs : float
        Sampling rate (Hz)

    Returns
    -------
    order : integer
        Order of filter

    """
    # TODO: Write a set of functions or stubs, all about order
    N = round(60 * 120 * fs)
    unit_pulse = np.zeros(N)
    unit_pulse[1] = 1
    n1 = round((band[0] * N//2) / (fs/2))
    n2 = round((band[1] * N//2) / (fs/2))
    ideal_fr = np.zeros(N)
    f = np.fft.fftfreq(N, 1/fs)
    ind = (f>= band[0])&(f<= band[1])
    ideal_fr[ind] = 1
    ideal_fr = ideal_fr[:N//2]
    prev_metric = np.inf
    for order in range(3, 21):
        impulse_response = butter_bandpass_filter(unit_pulse, band[0], band[1], fs, order)
        fr = abs(fftpack.fft(impulse_response))[:N//2]
        metric = np.sum((fr - ideal_fr)**2)**0.5
        best_order = order
        if (np.isnan(metric)) or (metric >= prev_metric):
            best_order -= 1
            break
        prev_metric = metric
    return best_order-1 # TODO: Think about it

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
