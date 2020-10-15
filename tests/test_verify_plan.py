# Copyright (C) 2017-2020 Aleksandr Popov

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
from dsplab.flow.verify import check_plan, VerifyError


SCHEMA_FILE_NAME = 'dsplab/data/plan-schema.json'


class TestVerification(unittest.TestCase):
    def test_empty(self):
        plan_dict = {}
        with self.assertRaises(VerifyError):
            check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_empty_nodes(self):
        plan_dict = {
            'nodes': [],
        }
        with self.assertRaises(VerifyError):
            check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_wrong_node_brakes_plan(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'wrong_key': 12345,
                },
            ],

            'inputs': ['a'],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError):
            check_plan(plan_dict, SCHEMA_FILE_NAME)
