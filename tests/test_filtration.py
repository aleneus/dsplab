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

import unittest
from .context import dsplab
import numpy as np
from dsplab import filtration as flt

class TestHaarOneStep(unittest.TestCase):
    def test_haar_one_step_even_len(self):
        t = [0,1,2,3,4,5]
        x = [1,2,3,4,5,6]
        x_s, x_d, t_new = flt.haar_one_step(x, t)
        self.assertEqual(len(x_s), 3)
        self.assertEqual(len(x_d), 3)
        self.assertEqual(len(t_new), 3)

    def test_haar_one_step_sum_of_values(self):
        t = [0,1,2,3,4,5]
        x = [1,2,3,4,5,6]
        x_s, x_d, t_new = flt.haar_one_step(x, t, denominator=2)
        self.assertEqual(sum(x_s), 10.5)
        self.assertEqual(sum(x_d), -1.5)
        
    def test_haar_one_step_odd_len(self):
        t = [0,1,2,3,4,5,6]
        x = [1,2,3,4,5,6,7]
        x_s, x_d, t_new = flt.haar_one_step(x, t)
        self.assertEqual(len(x_s), 3)
        self.assertEqual(len(x_d), 3)
        self.assertEqual(len(t_new), 3)

class TestHaarScaling(unittest.TestCase):
    def test_haar_scaling_len_sum(self):
        t = [0,1,2,3,4,5,6,7]
        x = [1,2,3,4,5,6,7,8]
        x_resampled, t_new = flt.haar_scaling(x, t, 3)
        self.assertEqual(len(x_resampled), 1)
        self.assertEqual(sum(x_resampled), 4.5)

    def test_haar_scaling_time(self):
        t = [0,1,2,3,4,5,6,7]
        x = [1,2,3,4,5,6,7,8]
        x_resampled, t_new = flt.haar_scaling(x, t, 3)
        self.assertEqual(len(t_new), 1)
        self.assertEqual(t_new[0], 7)

class TestOrder(unittest.TestCase):
    def test_find_butt_bandpass_order_1(self):
        band = (1.93, 2.14)
        sampling_steps = 2
        fs = 50/2**sampling_steps
        order = flt.find_butt_bandpass_order(band, fs)
        self.assertTrue(order > 5)

    def test_find_butt_bandpass_order_2(self):
        band = (3.84, 4)
        sampling_steps = 2
        fs = 50/2**sampling_steps
        order = flt.find_butt_bandpass_order(band, fs)
        self.assertTrue(order > 5)

class TestButter(unittest.TestCase):
    def test_butter_lowpass_just_run(self):
        fs = 50
        cutoff = 10
        order = 5
        flt.butter_lowpass(cutoff, fs, order)
        self.assertTrue(True)

    def test_butter_lowpass_filter_just_run(self):
        fs = 50
        x = np.arange(1, 100, 1/fs)
        cutoff = 10
        order = 5
        flt.butter_lowpass_filter(x, cutoff, fs, order)
        self.assertTrue(True)

    def test_butter_bandpass_just_run(self):
        fs = 50
        order = 10
        lowcut = 5
        highcut = 10
        flt.butter_bandpass(lowcut, highcut, fs, order)
        self.assertTrue(True)
        
    def test_butter_bandpass_filter_just_run(self):
        fs = 50
        x = np.arange(1, 100, 1/fs)
        order = 10
        lowcut = 5
        highcut = 10
        flt.butter_bandpass_filter(x, lowcut, highcut, fs, order)
        self.assertTrue(True)
