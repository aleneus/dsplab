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
from dsplab import damping as dam
import generators as gen
import numpy as np

class TestDamping(unittest.TestCase):
    def test_damping_number(self):
        x = [0,0,3,2,1,0,0,0,0,5,4,3,2,1,0,0,0,0,2,1,0]
        ts, ds = dam.damping_triangles(x)
        self.assertEqual(len(ts) + len(ds), 3 + 3)

