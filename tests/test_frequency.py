# Copyright (C) 2013 -- 2017 Aleksandr Popov

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

import unittest
from .context import dsplab
from dsplab import frequency as freq
import generators as gen
import numpy as np

class TestFrequency(unittest.TestCase):
    def test_freq_stupid_harmonic(self):
        fs = 5
        x, t = gen.harmonic(600, fs, 0.05)
        f = freq.freq_stupid(x, fs)
        self.assertAlmostEqual(f, 0.05, places = 2)

    def test_freqs_stupid_number_of_values(self):
        fs = 5
        x = [(-1)**i for i in range(100)]
        freqs, t = freq.freqs_stupid(x, fs, window_width = 10, window_step = 5)
        self.assertEqual(len(freqs), 19)

    def test_freqs_stupid_empty_array_number_of_values(self):
        fs = 5
        x = []
        freqs, t = freq.freqs_stupid(x, fs, window_width = 10, window_step = 5)
        self.assertEqual(len(freqs), 0)

    def test_freqs_stupid_harmonic(self):
        fs = 25
        x, t = gen.harmonic(60*60, fs, 8)
        freqs, y = freq.freqs_stupid(
            x,
            fs,
            window_width = round(30*fs),
            window_step = round(30*fs/2)
        )
        self.assertAlmostEqual(np.average(freqs), 8, places = 1)

    def test_freqs_stupid_freqs_and_t_lengths_equal(self):
        fs = 5
        x = [(-1)**i for i in range(100)]
        freqs, t = freq.freqs_stupid(x, fs, window_width = 10, window_step = 5)
        self.assertEqual(len(freqs), len(t))
        
