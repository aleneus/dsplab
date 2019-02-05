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
from dsplab import envelope as env
import numpy as np

class TestDamping(unittest.TestCase):
    def test_envelope_by_extremums_len_of_result(self):
        x = np.array([0,1,0,-1,0,1,0,-1,0,1,0])
        e, t = env.envelope_by_extremums(x)
        self.assertEqual(len(e) + len(t), 5 + 5)

    def test_calc_hilbert_filter_len(self):
        h = env.hilbert_filter(3)
        self.assertEqual(len(h), 7)
