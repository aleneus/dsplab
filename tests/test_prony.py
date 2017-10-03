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

import unittest
from .context import dsplab
import numpy as np
from dsplab import prony

class TestDamping(unittest.TestCase):
    def test_prony_sum_length_of_result(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2, -2, 1, -1, 0, 0]
        L = 4
        ms, cs, es = prony.prony_decomp(x, L)
        self.assertEqual(len(ms) + len(cs) + len(es) == 4 + 4 + 4)

    def test_prony_sum_length_of_result(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2, -2, 1, -1, 0, 0]
        L = 4
        ms, cs, es = prony.prony_decomp(x, L)
        self.assertEqual(len(es[0]), len(x))

    def test_prony_wrong_number_of_components(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2, -2, 1, -1, 0, 0]
        L = len(x)//2 + 1
        res = prony.prony_decomp(x, L)
        self.assertEqual(res, None)