# Copyright (C) 2017 Aleksandr Popov

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
from dsplab import damping as dam
import numpy as np

class TestDamping(unittest.TestCase):
    def test_damping_empty_data(self):
        ds, ts = dam.damping_triangles([], 1)
        self.assertEqual(len(ds), 0)
        
    def test_damping_number(self):
        x = [0,0,2,3,2,1,0,0,0,2,5,4,3,2,1,0,0,0,1,2,1,0,0]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertEqual(len(ts) + len(ds), 3 + 3)

    def test_t_setted_damping_number(self):
        x = np.array([0,0,2,3,2,1,0,0,0])
        t = np.array([0,1,2,3,4,5,6,7,8])
        ds, ts = dam.damping_triangles(x, t = t)
        self.assertEqual(len(ds), 1)
        
    def test_damping_at_begin(self):
        x = [3,2,1,0,0,0]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertEqual(len(ts) + len(ds), 1 + 1)

    def test_damping_at_end(self):
        x = [0,0,2,5,4,3,2]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertEqual(len(ts) + len(ds), 1 + 1)

    def test_one_triangle(self):
        x = [0,0,5,4,3,2,1,0,0]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertTrue(
            (len(ts) + len(ds) == 2) and
            (ts[0] == 7) and
            (ds[0] == 1)
        )

    def test_two_triangles(self):
        x = [0,2,5,4,3,2,1,0,0,2,1,0,0]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertTrue(
            (len(ts) + len(ds) == 4) and
            (ds[0] == 1) and (ds[1] == 1)
        )

    def test_one_triangle_at_end(self):
        x = [0,0,0,0,0,2,5,4,3,2,1,0]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertTrue(
            (len(ds) == 1) and
            (ds[0] == 1)
        )
        
    def test_no_triangles(self):
        x = [1,1,1,1,2,3,4,5,5,5,5,5]
        ds, ts = dam.damping_triangles(x, 1)
        self.assertEqual(len(ds) + len(ts), 0)
