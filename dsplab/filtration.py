# Copyright (C) 2017 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from scipy.signal import butter, lfilter

def butter_lowpass(cutoff, fs, order):
    """ 
    Calculate a and b coefficients for Butterworth lowpass filter

    """
    nyq = 0.5 * fs
    b, a = butter(order, cutoff/nyq, btype='low')
    return b, a

def butter_lowpass_filter(x, cutoff, fs, order):
    """ 
    Filter signal with Butterworth lowpass filter

    """
    b, a = butter_lowpass(cutoff, fs, order)
    y = lfilter(b, a, x)
    return y

def butter_bandpass(lowcut, highcut, fs, order):
    """ 
    Calculate a and b coefficients for Butterworth bandpass filter

    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(x, lowcut, highcut, fs, order):
    """ 
    Filter signal with Butterworth bandpass filter

    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, x)
    return y
