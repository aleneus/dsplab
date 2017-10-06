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
from dsplab import io
import numpy as np
import os

class TestIO(unittest.TestCase):
    def test_read_signal_from_csv(self):
        with open('test.csv', 'w') as f:
            f.write("1;5\n")
            f.write("2;6\n")
            f.write("3;7\n")
        x, t = io.read_signal_from_csv("test.csv", start_line = 0)
        os.remove("test.csv")
        self.assertEqual(sum(x) - sum(t), 5+6+7 - (1+2+3))
