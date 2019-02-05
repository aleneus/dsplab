# Copyright (C) 2017-2019 Aleksandr Popov

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
from dsplab import modulation as mod

class TestPhasor(unittest.TestCase):
    def test_calc_freq_phasor_just_run(self):
        fs = 50
        t = np.arange(0, 20, 1/fs)
        x = np.cos(2*np.pi*1*t)
        mod.calc_freq_phasor(x, t, f_central=1, f_width=0.5)
        self.assertTrue(True)
