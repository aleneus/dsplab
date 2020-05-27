# Copyright (C) 2017-2020 Aleksandr Popov

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
from dsplab.modulation import (envelope_by_extremums,
                               digital_hilbert_filter, linint,
                               wave_lens, freqs_by_wave_len)


class TestModulation(unittest.TestCase):
    def test_envelope_by_extremums_len_of_result(self):
        x = np.array([0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0])
        e, t = envelope_by_extremums(x)
        self.assertEqual(len(e) + len(t), 5 + 5)

    def test_calc_hilbert_filter_len(self):
        h = digital_hilbert_filter(3)
        self.assertEqual(len(h), 3)


class TestFrequency(unittest.TestCase):
    def test_linint(self):
        t = np.array([0, 1, 3, 4, 6, 7, 9])
        x = np.array([0, 1, 3, 4, 6, 7, 9])
        t_new = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        x_new = linint(x, t, t_new)
        self.assertEqual(sum(x_new), 45)

    def test_linint_all_empty(self):
        t = np.array([])
        x = np.array([])
        t_new = np.array([])
        x_new = linint(x, t, t_new)
        self.assertEqual(len(x_new), 0)

    def test_linint_nans(self):
        t = np.array([0, 1, 3, 4, 6, 7])
        x = np.array([0, 1, 3, 4, 6, 7])
        t_new = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        x_new = linint(x, t, t_new)
        self.assertEqual(np.nansum(x_new), 28)
        self.assertEqual(len(x_new), 10)

    def test_wave_lens(self):
        t = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        x = np.array([1, -1,  1, -1,  1, -1,  1, -1,  1, -1,  1])
        wl, t_wl = wave_lens(x, t)
        self.assertEqual(len(wl), 9)
        self.assertEqual(len(t_wl), 9)
        self.assertEqual(sum(wl), 9)
        self.assertEqual(sum(t_wl), 27)

    def test_freqs_by_wave_len(self):
        t = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        x = np.array([1, -1,  1, -1,  1, -1,  1, -1,  1, -1,  1])
        f, t_f = freqs_by_wave_len(x, t)
        self.assertEqual(len(f), 9)
        self.assertEqual(len(t_f), 9)
        self.assertEqual(np.sum(f), 9)


unittest.main()
