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
from dsplab.helpers import is_iterable


class Test_is_iterable(unittest.TestCase):
    def test_list(self):
        self.assertTrue(is_iterable([1, 2, 3]))

    def test_single_value(self):
        self.assertFalse(is_iterable(1))

    def test_none(self):
        self.assertFalse(is_iterable(None))

    def test_nparray(self):
        self.assertTrue(is_iterable(np.array([1, 2, 3])))
