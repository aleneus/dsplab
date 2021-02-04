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
from dsplab.modulation import (harm, digital_hilbert_filter, linint,
                               envelope_by_extremums, wave_lens,
                               freqs_by_wave_len, freq_by_zeros,
                               freq_by_extremums)


class TestHarm(unittest.TestCase):
    def test_simple_harmonic(self):
        rate = 50
        length = 60
        amp = 1

        xs, ts = harm(length=length, sample_rate=rate, amp=amp, freq=1)
        self.assertEqual(len(xs), len(ts))
        self.assertEqual(len(xs), length*rate)
        self.assertAlmostEqual(max(xs), amp)
        self.assertAlmostEqual(min(xs), -amp)
        self.assertAlmostEqual(sum(xs), 0)
        self.assertAlmostEqual(ts[1]-ts[0], 1/rate)

    def test_amplitude(self):
        amp = 2.5

        xs = harm(length=60, sample_rate=50, amp=amp, freq=1)[0]
        self.assertAlmostEqual(max(xs), amp)
        self.assertAlmostEqual(min(xs), -amp)
        self.assertAlmostEqual(sum(xs), 0)

    def test_frequency(self):
        """Scenario: frequency and sample rate are equal."""
        xs = harm(length=60, sample_rate=1, amp=1, freq=1)[0]
        self.assertAlmostEqual(sum(xs), 60)

    def test_noised_amplitude(self):
        def noise(t):
            return 1

        xs = harm(length=60, sample_rate=50, amp=1, freq=1, noise_a=noise)[0]
        self.assertAlmostEqual(max(xs), 2)
        self.assertAlmostEqual(min(xs), -2)

    def test_noised_phase(self):
        def noise(t):
            return np.pi / 2

        xs = harm(length=60, sample_rate=1, amp=1, freq=1, noise_f=noise)[0]
        self.assertAlmostEqual(sum(xs), 0)
        self.assertAlmostEqual(max(xs), 0)
        self.assertAlmostEqual(min(xs), 0)


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

    def test_freq_by_zeros(self):
        x = np.array([1, 0, -1,  0])
        self.assertAlmostEqual(freq_by_zeros(x, 4), 1)


class TestFreqByExtremums(unittest.TestCase):
    def test_short_signal(self):
        raised = False
        try:
            freq_by_extremums([1, 0], 4)
        except ValueError:
            raised = True

        self.assertTrue(raised)

    def test_single_wave(self):
        x = np.array([1, 0, -1,  0])
        self.assertAlmostEqual(freq_by_extremums(x, 4), 1)
