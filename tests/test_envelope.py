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
from dsplab import envelope as env
import numpy as np

class TestDamping(unittest.TestCase):
    def test_envelope_by_max_len_of_result(self):
        x = [1,2,1,2,1,2,1]
        e, t = env.envelope_by_max(x)
        self.assertEqual(len(e) + len(t), 3 + 3)

    def test_envelope_by_max_len_of_result_end(self):
        x = [1,2,1,2,1,2]
        e, t = env.envelope_by_max(x)
        self.assertEqual(len(e) + len(t), 3 + 3)

    def test_envelope_by_max_sum_of_result(self):
        x = [1,2,1,2,1,2,1]
        e, t = env.envelope_by_max(x)
        self.assertEqual(sum(e) + sum(t), 6 + 9)

    def test_envelope_hilbert(self):
        x = [0 for _ in range(100)]
        e = env.envelope_hilbert(x)
        self.assertEqual(len(e), 100)

        
