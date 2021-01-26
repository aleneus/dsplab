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
from dsplab.flow.verify import _check_plan_schema, _load_schema
from dsplab.flow.verify import _check_node


PLAN_SCHEMA_FILE_NAME = 'dsplab/data/plan-schema.json'
NODE_SCHEMA_FILE_NAME = 'dsplab/data/node-schema.json'


class Test__check_plan_cheme(unittest.TestCase):
    def setUp(self):
        def check(p):
            _check_plan_schema(p, _load_schema(PLAN_SCHEMA_FILE_NAME))

        self.check = check

    def test_ok_minimal(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'work': {'worker': {}}},
            ],

            'outputs': ['a'],
        }
        self.check(plan_dict)

    def test_empty(self):
        plan_dict = {}
        with self.assertRaises(VerifyError):
            self.check(plan_dict)

    def test_empty_nodes(self):
        plan_dict = {
            'nodes': [],
        }
        with self.assertRaises(VerifyError):
            self.check(plan_dict)

    def test_wrong_node_brakes_plan(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'wrong_key': 12345},
            ],
            'inputs': ['a'],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError):
            self.check(plan_dict)


class Test_check_plan(unittest.TestCase):
    def setUp(self):
        def check(p):
            check_plan(p, PLAN_SCHEMA_FILE_NAME)

        self.check = check

    def test_schema_error(self):
        plan_dict = {}
        with self.assertRaises(VerifyError):
            self.check(plan_dict)

    def test_node_error(self):
        plan_dict = {
            'nodes': [
                {'id': 'a', 'class': 'WorkNode'},
            ],
            'outputs': ['a'],
        }
        with self.assertRaises(VerifyError) as cm:
            self.check(plan_dict)

        self.assertEqual(cm.exception.__str__(), "No work in node a")

    def test_duplicated_ids(self):
        plan_dict = {
            'nodes': [
                {'id': 'b', 'work': {'worker': {}}},
                {'id': 'b', 'work': {'worker': {}}},
            ],
            'outputs': ['b'],
        }
        with self.assertRaises(VerifyError) as cm:
            self.check(plan_dict)
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
            self.check(plan_dict)
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
            self.check(plan_dict)
        self.assertEqual(cm.exception.__str__(), "Unknown plan output: c")

    def test_unknown_node_input(self):
        plan_dict = {
            'nodes': [
                {'id': 'b', 'work': {'worker': {}}, 'inputs': ['c']},
            ],
            'outputs': ['b'],
        }
        with self.assertRaises(VerifyError) as cm:
            self.check(plan_dict)
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
            self.check(plan_dict)
        self.assertEqual(cm.exception.__str__(), "Node a uses itself as input")


class Test__check_node(unittest.TestCase):
    def setUp(self):
        def check(n):
            _check_node(n, ids={'a': True, 'b': True})

        self.check = check

    def test_work_node_minimal_ok(self):
        node_dict = {
            'id': 'a',
            'class': 'WorkNode',
            'work': {'worker': {}},
        }
        self.check(node_dict)

    def test_map_node_minimal_ok(self):
        node_dict = {
            'id': 'a',
            'class': 'MapNode',
            'work': {'worker': {}},
        }
        self.check(node_dict)

    def test_select_node_minimal_ok(self):
        node_dict = {
            'id': 'b',
            'class': 'SelectNode',
            'inputs': ['a'],
        }
        self.check(node_dict)

    def test_pack_node_minimal_ok(self):
        node_dict = {
            'id': 'a',
            'class': 'PackNode',
        }
        self.check(node_dict)

    def test_pass_node_minimal_ok(self):
        node_dict = {
            'id': 'a',
            'class': 'PassNode',
        }
        self.check(node_dict)

    def test_unknown_class(self):
        node_dict = {
            'id': 'a',
            'class': 'the middle class',
        }

        self.check(node_dict)

    def test_work_is_default_class(self):
        node_dict = {
            'id': 'a',
        }
        with self.assertRaises(VerifyError) as cm:
            self.check(node_dict)
        self.assertEqual(cm.exception.__str__(), "No work in node a")

    def test_work_node_must_have_work(self):
        node_dict = {
            'id': 'a',
            'class': 'WorkNode',
        }
        with self.assertRaises(VerifyError) as cm:
            self.check(node_dict)

        self.assertEqual(cm.exception.__str__(), "No work in node a")
