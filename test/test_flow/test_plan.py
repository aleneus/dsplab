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
from dsplab.flow.plan import Node
from dsplab.flow.plan import get_plan_from_dict


class TestNode(unittest.TestCase):
    def test_result_info(self):
        n = Node()
        n.result_info = "Signal"
        self.assertEqual(n.result_info, "Signal")


class Test_get_plan_from_dict(unittest.TestCase):
    def test_empty(self):
        plan_dict = {
            'nodes': [],
            'outputs': [],
        }
        get_plan_from_dict(plan_dict)

    def test_description_empty(self):
        plan_dict = {
            'nodes': [],
            'outputs': [],
        }
        plan = get_plan_from_dict(plan_dict)
        self.assertEqual(plan.descr, '')

    def test_description_not_empty(self):
        plan_dict = {
            'descr': 'My plan',
            'nodes': [],
            'outputs': [],
        }
        plan = get_plan_from_dict(plan_dict)
        self.assertEqual(plan.descr, 'My plan')

    def test_single_pass_node(self):
        plan_dict = {
            'descr': 'My plan',
            'nodes': [
                {
                    'id': 'a',
                    'class': 'PassNode',
                },
            ],
            'outputs': [],
        }
        plan = get_plan_from_dict(plan_dict)
        self.assertEqual(plan.descr, 'My plan')

    def test_result_description(self):
        plan_dict = {
            'descr': 'My plan',
            'nodes': [
                {
                    'id': 'a',
                    'class': 'PassNode',
                    'result': 'my result',
                },
            ],
            'outputs': ['a'],
        }
        plan = get_plan_from_dict(plan_dict)
        self.assertEqual(plan.get_outputs()[0].get_result_info(), 'my result')
