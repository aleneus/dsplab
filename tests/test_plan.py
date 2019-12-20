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
from context import dsplab
from dsplab.plan import Node


class TestNode(unittest.TestCase):
    def test_deprecated_info(self):
        n = Node()
        info = n.info()
        self.assertTrue(info is not None)

    def test_result_info(self):
        n = Node()
        n.result_info = "Signal"
        self.assertEqual(n.result_info, "Signal")


unittest.main()
