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
from dsplab.prony import prony_decomp


class TestProny(unittest.TestCase):
    def test_prony_sum_length_of_result(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8,
             4, -4, 2, -2, 1, -1, 0, 0]
        L = 4
        ms, cs, es = prony_decomp(x, L)
        self.assertEqual(len(ms) + len(cs) + len(es), 4 + 4 + 4)

    def test_prony_length_of_components(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8,
             4, -4, 2, -2, 1, -1, 0, 0]
        L = 4
        ms, cs, es = prony_decomp(x, L)
        self.assertEqual(len(es[0]), len(x))

    def test_prony_wrong_number_of_components(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8,
             4, -4, 2, -2, 1, -1, 0, 0]
        L = len(x)//2 + 1
        res = prony_decomp(x, L)
        self.assertEqual(res, None)

    def test_prony_double_number_of_components_equal_to_n(self):
        x = [255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8,
             4, -4, 2, -2, 1, -1, 0, 0]
        L = 10
        ms, cs, es = prony_decomp(x, L)
        self.assertEqual(len(ms) + len(cs) + len(es), 10 + 10 + 10)
