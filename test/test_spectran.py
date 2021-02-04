# Copyright (C) 2017-2021 Aleksandr Popov
# Copyright (C) 2021 Kirill Butin

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
import numpy as np
from dsplab.spectran import spectrum, stft, calc_specgram


class TestSpectrum(unittest.TestCase):
    def test_spectrum_len(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        X, f_X = spectrum(x, sample_rate=1)
        self.assertEqual(len(x), len(X))

    def test_spectrum_one_side_len(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        X, f_X = spectrum(x, sample_rate=1, one_side=True)
        self.assertEqual(len(x)//2, len(X))

    def test_spectrum_need_expand_len(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        X, f_X = spectrum(x, sample_rate=1, extra_len=16)
        self.assertEqual(16, len(X))


class TestSTFT(unittest.TestCase):
    def test_stft_number_of_spectrums_no_overlap(self):
        fs = 1
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        Xs = stft(x, fs, 2, 2, window='hanning', nfft=None, padded=False)
        self.assertEqual(len(Xs), 5)

    def test_stft_number_of_spectrums_overlap(self):
        fs = 1
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        Xs = stft(x, fs, 2, 1, window='hanning', nfft=None, padded=False)
        self.assertEqual(len(Xs), 9)

    def test_stft_len_of_spectrum_dont_add_zeros_to_segments(self):
        fs = 1
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        Xs = stft(x, fs, 2, 2, window='hanning', nfft=None, padded=False)
        self.assertEqual(len(Xs[0]), 2)

    def test_stft_len_of_spectrum_add_zeros_to_segments(self):
        fs = 1
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        Xs = stft(x, fs, 2, 2, window='hanning', nfft=4, padded=False)
        self.assertEqual(len(Xs[0]), 4)

    def test_stft_padding_true(self):
        fs = 1
        x = np.array([0, 1, 2, 3, 4, 5, 6])
        Xs = stft(x, fs, 3, 3, window='hanning', nfft=None, padded=True)
        self.assertEqual(len(Xs), 3)

    def test_stft_short_signal(self):
        x = np.linspace(0, 1, 100)
        Xs = stft(x, sample_rate=1, nseg=256, nstep=128)
        self.assertEqual(len(Xs), 0)


class TestSpecgram(unittest.TestCase):
    def test_calc_specgram_just_run(self):
        x = np.linspace(0, 100, 1024)
        calc_specgram(x)
        self.assertTrue(True)

    def test_calc_specgram_short_signal(self):
        x = np.linspace(0, 1, 100)
        Xs, t = calc_specgram(x, nseg=256)
        self.assertEqual(len(Xs), 0)
        self.assertEqual(len(t), 0)

    def test_calc_specgram_len_signal_and_nseg_are_equal(self):
        x = np.linspace(0, 1, 256)
        Xs, t = calc_specgram(x, nseg=256)
        self.assertEqual(len(Xs[0]), 1)
        self.assertEqual(len(t), 1)

    def test_calc_specgram_time_used_just_run(self):
        t = np.linspace(0, 100, 1024)
        x = np.cos(t)
        calc_specgram(x, tdata=t)
        self.assertTrue(True)

    def test_calc_specgram_bound_used_just_run(self):
        fs = 50
        t = np.arange(0, 20, 1/fs)
        x = np.cos(2*np.pi*1*t)
        calc_specgram(x, tdata=t, freq_bounds=(0.5, 1.5))
        self.assertTrue(True)

    def test_calc_specgram_fs_used_just_run(self):
        fs = 50
        t = np.arange(0, 20, 1/fs)
        x = np.cos(2*np.pi*1*t)
        calc_specgram(x, sample_rate=fs)
        self.assertTrue(True)
