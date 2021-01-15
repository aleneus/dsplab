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
    def test_ok_minimal(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'work': {'worker': {}}},
            ],

            'outputs': ['a'],
        }
        check_plan(plan_dict, SCHEMA_FILE_NAME)

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
        # Note: if 'empty work' error will raised earlier, then delete
        # this test

        plan_dict = {
            'nodes': [
                {'id': 'a', 'wrong_key': 12345},
            ],
            'inputs': ['a'],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError):
            check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_duplicated_ids(self):
        plan_dict = {
            'nodes': [
                {'id': 'b', 'work': {'worker': {}}},
                {'id': 'b', 'work': {'worker': {}}},
            ],
            'outputs': ['b'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "Duplicated ID: b")

    def test_unknown_plan_input(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'work': {'worker': {}}},
            ],
            'inputs': ['b'],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "Unknown plan input: b")

    def test_unknown_plan_output(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'work': {'worker': {}}},
            ],
            'inputs': ['a'],
            'outputs': ['c'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "Unknown plan output: c")

    def test_unknown_node_input(self):
        plan_dict = {
            'nodes': [
                {'id': 'b', 'work': {'worker': {}}, 'inputs': ['c']},
            ],
            'outputs': ['b'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "Unknown input c in node b")

    def test_loop(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'work': {'worker': {}}, 'inputs': ['a']},
            ],
            'inputs': ['a'],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "Node a uses itself as input")


class TestVerification_ClassOfNode(unittest.TestCase):
    def test_work_node_minimal_ok(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'class': 'WorkNode',
                    'work': {'worker': {}},
                },
            ],
            'outputs': ['a'],
        }
        check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_map_node_minimal_ok(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'class': 'MapNode',
                    'work': {'worker': {}},
                },
            ],
            'outputs': ['a'],
        }
        check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_select_node_minimal_ok(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'work': {'worker': {}},
                },

                {
                    'id': 'b',
                    'class': 'SelectNode',
                    'inputs': ['a'],
                },
            ],

            'outputs': ['b'],
        }
        check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_pack_node_minimal_ok(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'class': 'PackNode',
                },
            ],

            'outputs': ['a'],
        }
        check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_pass_node_minimal_ok(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'class': 'PassNode',
                },
            ],

            'outputs': ['a'],
        }
        check_plan(plan_dict, SCHEMA_FILE_NAME)

    def test_unknown_class(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'class': 'the middle class',
                },
            ],

            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError):
            check_plan(plan_dict, SCHEMA_FILE_NAME)


class TestVerification_DependOnClass(unittest.TestCase):
    def test_work_is_default_class(self):
        plan_dict = {
            'nodes': [
                {'id': 'a'},
            ],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "No work in node a")

    def test_work_node_must_have_work(self):
        plan_dict = {
            'nodes': [
                {
                    'id': 'a',
                    'class': 'WorkNode',
                },
            ],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError) as cm:
            check_plan(plan_dict, SCHEMA_FILE_NAME)
        self.assertEqual(cm.exception.__str__(), "No work in node a")
