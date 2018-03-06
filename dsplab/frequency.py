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

# TODO: rename this module

import numpy as np

def freq_by_extremums(x, fs):
    """
    Calculate frequency of oscillating signal by extremums.

    Parameters
    ----------
    x : array_like
        Values of input signals
    fs : float
        Sampling frequency (Hz)

    Returns
    -------
    freq : float
        Frequency

    """
    T = len(x)/fs
    n_max = 0
    n_min = 0
    for x_p, x_c, x_n in zip(x[:-2], x[1:-1], x[2:]):
        if (x_p < x_c) and (x_c >= x_n):
            n_max += 1
        if (x_p > x_c) and (x_c <= x_n):
            n_min += 1
    n = (n_max + n_min) / 2
    return n / T

def freq_by_zeros(x, fs):
    """
    Calculate frequency of oscillating signal by zeros. Signal must be detrended before.

    # TODO: par and ret
    """
    T = len(x)/fs
    n = 0
    for x_p, x_c in zip(x[:-1], x[1:]):
        if x_p * x_c < 0:
            n += 1
    return n / 2 / T

def freqs_stupid(x, fs, window_width = 1024, window_step = 512):
    """
    Calculate an array of frequencies of oscillating signal using window

    Parameters
    ----------
    x : array_like
        Values of input signals
    fs : float
        Sampling frequency (Hz)
    window_width : integer
        Width of window (Samples)
    window_step : integer
        Distance between centers of nearby windows (Samples)

    Returns
    -------
    freqs : np.ndarray
        Frequency values
    t_new : time values

    """
    freqs = []
    t_new = []
    start = 0
    stop = window_width
    if stop > len(x):
        return freqs, t_new
    while True:
        f = freq_by_zeros(x[start : stop], fs)
        freqs.append(f)
        t_new.append((stop-1)/fs)
        start += window_step
        stop += window_step
        if stop > len(x):
            break
    return np.array(freqs), np.array(t_new)

def linint(x, t, t_new, cut_nans=True):
    """
    Find values of x in t_new points.

    Parameters
    ----------
    x : np.ndarray
        Signal values.
    t : np.ndarray
        Time values.
    t_new : np.ndarray
        New time values.
    cat_nans : boolean
        If True, the nan values at the begin and at the end of produced array will removed. 
        Such values will be appear if t_new is wider than t.
 
    Returns
    -------
    x_new : np.ndarray
        New signal values.
 
    """
    x_new = np.zeros(len(t_new)) * np.nan
    for x_p, t_p, x_c, t_c in zip(x[:-1], t[:-1], x[1:], t[1:]):
        k = (x_c - x_p) / (t_c - t_p)
        b = x_p - k*t_p
        ind = (t_new>=t_p)&(t_new<=t_c) 
        x_new[ind] = k*t_new[ind] + b # TODO: rewrite it not using this ind, try to do it real-time
    return x_new

def wave_lens(x, t):
    """
    Calculate wave lengths of signal by space between zeros.

    Parameters
    ----------
    x : np.ndarray
        Signal values.
    t : np.ndarray
        Time values.

    Returns
    -------
    lens : np.ndarray
        Wave lengths.
    t_lent : np.ndarray
        Time values.
    
    """
    tms = []
    for t_c, x_p, x_c in zip(t[1:], x[:-1], x[1:]):
        if x_p * x_c < 0:
            tms.append(t_c)
    # TODO: replace diff by something like real-time, do all in one cycle
    lens = np.diff(tms) * 2
    t_lens = np.array(tms[1:])
    return lens, t_lens

def freqs_by_wave_len(x, t, cut_nans=True):
    """
    Calculate frequencies using lenghs of waves and linear interpolation.

    Parameters
    ----------
    x : np.ndarray
        Signal values.
    t : np.ndarray
        Time values.
    cut_nans : boolean
        If True, the nan values at the ends of the of the produced array will removed. 

    Returns
    -------
    freqs : np.ndarray
        Freqs values
    
    """
    wl, t_wl = wave_lens(x, t)
    freqs = 1/linint(wl, t_wl, t)
    if cut_nans:
        freqs_cut = []
        t_cut = []
        for (f, tt) in zip(freqs, t): # TODO: name tt
            if f==f:
                freqs_cut.append(f)
                t_cut.append(tt)
        return np.array(freqs_cut), t_cut
    return freqs, t

