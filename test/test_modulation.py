# Copyright (C) 2017-2022 Aleksandr Popov
# Copyright (C) 2021-2022 Kirill Butin

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
from dsplab import modulation as mod


class Test_harm(unittest.TestCase):
    def test_amplitude_and_rate(self):
        rate = 50
        length = 120
        amp = 2.5

        xs, ts = mod.harm(length=length, sample_rate=rate, amp=amp, freq=1)
        self.assertEqual(len(xs), len(ts))
        self.assertEqual(len(xs), length*rate)
        self.assertAlmostEqual(max(xs), amp)
        self.assertAlmostEqual(min(xs), -amp)
        self.assertAlmostEqual(sum(xs), 0)
        self.assertAlmostEqual(ts[1]-ts[0], 1/rate)

    def test_frequency(self):
        xs = mod.harm(length=60, sample_rate=1, amp=1, freq=1)[0]
        self.assertAlmostEqual(sum(xs), 60)

    def test_noised_amplitude(self):
        xs = mod.harm(length=60, sample_rate=50, amp=1, freq=1,
                      noise_amp=lambda: 1)[0]
        self.assertAlmostEqual(max(xs), 2)
        self.assertAlmostEqual(min(xs), -2)

    def test_noised_phase(self):
        xs = mod.harm(length=60, sample_rate=1, amp=1, freq=1,
                      noise_ph=lambda: np.pi/2)[0]
        self.assertAlmostEqual(sum(xs), 0)
        self.assertAlmostEqual(max(xs), 0)
        self.assertAlmostEqual(min(xs), 0)


class Test_amp_mod(unittest.TestCase):
    def test_empty(self):
        xs, ts = mod.amp_mod(0, 50, lambda t: 1, 10)
        self.assertEqual(len(xs), 0)
        self.assertEqual(len(ts), 0)

    def test_result_len(self):
        xs, ts = mod.amp_mod(1, 50, lambda t: 1, 10)
        self.assertEqual(len(xs), 50)
        self.assertEqual(len(ts), 50)

    def test_noise_amp(self):
        xs = mod.amp_mod(1, 50, lambda t: 1, 1, noise_amp=lambda: 1)[0]
        self.assertEqual(max(xs), 2)
        self.assertEqual(min(xs), 0)

    def test_noise_ph_touch(self):
        xs = mod.amp_mod(1, 50, lambda t: 1, 1, noise_ph=lambda: 0)[0]
        self.assertEqual(len(xs), 50)


class Test_freq_mod(unittest.TestCase):
    def test_touch(self):
        xs, phs, ts = mod.freq_mod(1, 50, 1, lambda t: 10,
                                   noise_amp=lambda: 1, noise_ph=lambda: 0)
        self.assertEqual(len(xs), 50)
        self.assertEqual(len(phs), 50)
        self.assertEqual(len(ts), 50)


class Test_phase_mod(unittest.TestCase):
    def test_touch(self):
        xs, ts = mod.phase_mod(1, 50, 1, 10, lambda t: 10,
                               noise_amp=lambda: 1, noise_ph=lambda: 0)
        self.assertEqual(len(xs), 50)
        self.assertEqual(len(ts), 50)


class Test_freq_amp_mod(unittest.TestCase):
    def test_touch(self):
        xs, phs, ts = mod.freq_amp_mod(1, 50, lambda t: 1, lambda t: 10)
        self.assertEqual(len(xs), 50)
        self.assertEqual(len(phs), 50)
        self.assertEqual(len(ts), 50)


class Test_envelope_by_extremums(unittest.TestCase):
    def test_result_len(self):
        x = np.array([0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0])
        e, t = mod.envelope_by_extremums(x)
        self.assertEqual(len(e) + len(t), 5 + 5)


class Test_digital_hilbert_filter(unittest.TestCase):
    def test_filter_len(self):
        self.assertEqual(len(mod.digital_hilbert_filter(3)), 3)


class Test_linint(unittest.TestCase):
    def test_empty(self):
        t = np.array([])
        x = np.array([])
        t_new = np.array([])
        x_new = mod.linint(x, t, t_new)
        self.assertEqual(len(x_new), 0)

    def test_not_empty(self):
        t = np.array([0, 1, 3, 4, 6, 7, 9])
        x = np.array([0, 1, 3, 4, 6, 7, 9])
        t_new = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        x_new = mod.linint(x, t, t_new)
        self.assertEqual(sum(x_new), 45)

    def test_nans(self):
        t = np.array([0, 1, 3, 4, 6, 7])
        x = np.array([0, 1, 3, 4, 6, 7])
        t_new = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        x_new = mod.linint(x, t, t_new)
        self.assertEqual(np.nansum(x_new), 28)
        self.assertEqual(len(x_new), 10)


class Test_wave_lens(unittest.TestCase):
    def test_touch(self):
        t = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        x = np.array([1, -1,  1, -1,  1, -1,  1, -1,  1, -1,  1])
        wl, t_wl = mod.wave_lens(x, t)
        self.assertEqual(len(wl), 9)
        self.assertEqual(len(t_wl), 9)
        self.assertEqual(sum(wl), 9)
        self.assertEqual(sum(t_wl), 27)


class Test_freqs_by_wave_len(unittest.TestCase):
    def test_touch(self):
        t = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        x = np.array([1, -1,  1, -1,  1, -1,  1, -1,  1, -1,  1])
        f, t_f = mod.freqs_by_wave_len(x, t)
        self.assertEqual(len(f), 9)
        self.assertEqual(len(t_f), 9)
        self.assertEqual(np.sum(f), 9)


class Test_freq_by_zeros(unittest.TestCase):
    def test_touch(self):
        x = np.array([1, 0, -1,  0])
        self.assertAlmostEqual(mod.freq_by_zeros(x, 4), 1)


class TestFreqByExtremums(unittest.TestCase):
    def test_short_signal(self):
        with self.assertRaises(ValueError):
            mod.freq_by_extremums([1, 0], 4)

    def test_single_wave(self):
        x = np.array([1, 0, -1,  0])
        self.assertAlmostEqual(mod.freq_by_extremums(x, 4), 1)
