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
from dsplab import spectran as sp

class TestSpectrum(unittest.TestCase):
    def test_spectrum_len(self):
        x = [1,2,3,4,5,6,7,8]
        X = sp.spectrum(x)
        self.assertEqual(len(x), len(X))

class TestExpandTo(unittest.TestCase):
    def test_expand_to(self):
        x = [1,1,1,1,1,1,1,1]
        xe = sp.expand_to(x, 16)
        self.assertEqual(len(xe), 16)
        self.assertEqual(sum(x), sum(xe))

class TestSTFT(unittest.TestCase):
    def test_stft_number_of_spectrums_no_overlap(self):
        dt = 1
        x = np.array([0,1,2,3,4,5,6,7,8,9])
        Xs = sp.stft(x, dt, 2, 2, window='hanning', nfft=None, padded=False)
        self.assertEqual(len(Xs), 5)
        
    def test_stft_number_of_spectrums_overlap(self):
        dt = 1
        x = np.array([0,1,2,3,4,5,6,7,8,9])
        Xs = sp.stft(x, dt, 2, 1, window='hanning', nfft=None, padded=False)
        self.assertEqual(len(Xs), 9)
        
    def test_stft_len_of_spectrum_dont_add_zeros_to_segments(self):
        dt = 1
        x = np.array([0,1,2,3,4,5,6,7,8,9])
        Xs = sp.stft(x, dt, 2, 2, window='hanning', nfft=None, padded=False)
        self.assertEqual(len(Xs[0]), 2)

    def test_stft_len_of_spectrum_add_zeros_to_segments(self):
        dt = 1
        x = np.array([0,1,2,3,4,5,6,7,8,9])
        Xs = sp.stft(x, dt, 2, 2, window='hanning', nfft=4, padded=False)
        self.assertEqual(len(Xs[0]), 4)

    def test_stft_padding_true(self):
        dt = 1
        x = np.array([0,1,2,3,4,5,6])
        Xs = sp.stft(x, dt, 3, 3, window='hanning', nfft=None, padded=True)
        self.assertEqual(len(Xs), 3)