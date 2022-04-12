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
from dsplab.flow.verify import check_plan, VerifyError
from dsplab.flow.verify import _check_plan_schema, _load_schema
from dsplab.flow.verify import _check_node


PLAN_SCHEMA_FILE_NAME = 'dsplab/data/plan-schema.json'


class Test__check_plan_cheme(unittest.TestCase):
    def setUp(self):
        def check(conf):
            _check_plan_schema(conf, _load_schema(PLAN_SCHEMA_FILE_NAME))

        self.check = check

    def test_ok_minimal(self):
        self.check({
                'nodes': [
                    {'id': 'a', 'work': {'worker': {}}},
                ],

                'outputs': ['a'],
            })

    def test_empty(self):
        with self.assertRaises(VerifyError):
            self.check({})

    def test_empty_nodes(self):
        with self.assertRaises(VerifyError):
            self.check({
                'nodes': [],
            })

    def test_wrong_node_brakes_plan(self):
        with self.assertRaises(VerifyError):
            self.check({
                'nodes': [
                    {'id': 'a', 'wrong_key': 12345},
                ],
                'inputs': ['a'],
                'outputs': ['a'],
            })


class Test_check_plan(unittest.TestCase):
    def setUp(self):
        self.check = check_plan

    def test_schema_error(self):
        with self.assertRaises(VerifyError):
            self.check({})

    def test_node_error(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'nodes': [
                    {'id': 'a', 'class': 'WorkNode'},
                ],
                'outputs': ['a'],
            })

        self.assertEqual(cm.exception.__str__(), "No work in node a")

    def test_duplicated_ids(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'nodes': [
                    {'id': 'b', 'work': {'worker': {}}},
                    {'id': 'b', 'work': {'worker': {}}},
                ],
                'outputs': ['b'],
            })
        self.assertEqual(cm.exception.__str__(), "Duplicated ID: b")

    def test_unknown_plan_input(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'nodes': [
                    {'id': 'a', 'work': {'worker': {}}},
                ],
                'inputs': ['b'],
                'outputs': ['a'],
            })
        self.assertEqual(cm.exception.__str__(), "Unknown plan input: b")

    def test_unknown_plan_output(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'nodes': [
                    {'id': 'a', 'work': {'worker': {}}},
                ],
                'inputs': ['a'],
                'outputs': ['c'],
            })
        self.assertEqual(cm.exception.__str__(), "Unknown plan output: c")

    def test_unknown_node_input(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'nodes': [
                    {'id': 'b', 'work': {'worker': {}}, 'inputs': ['c']},
                ],
                'outputs': ['b'],
            })
        self.assertEqual(cm.exception.__str__(), "Unknown input c in node b")

    def test_loop(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'nodes': [
                    {'id': 'a', 'work': {'worker': {}}, 'inputs': ['a']},
                ],
                'inputs': ['a'],
                'outputs': ['a'],
            })
        self.assertEqual(cm.exception.__str__(), "Node a uses itself as input")


class Test__check_node(unittest.TestCase):
    def setUp(self):
        def check(conf):
            _check_node(conf, ids={'a': True, 'b': True})

        self.check = check

    def test_work_node_minimal_ok(self):
        self.check({
            'id': 'a',
            'class': 'WorkNode',
            'work': {'worker': {}},
        })

    def test_map_node_minimal_ok(self):
        self.check({
            'id': 'a',
            'class': 'MapNode',
            'work': {'worker': {}},
        })

    def test_select_node_minimal_ok(self):
        self.check({
            'id': 'b',
            'class': 'SelectNode',
            'inputs': ['a'],
        })

    def test_pack_node_minimal_ok(self):
        self.check({
            'id': 'a',
            'class': 'PackNode',
        })

    def test_pass_node_minimal_ok(self):
        self.check({
            'id': 'a',
            'class': 'PassNode',
        })

    def test_unknown_class(self):
        self.check({
            'id': 'a',
            'class': 'the middle class',
        })

    def test_work_is_default_class(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'id': 'a',
            })
        self.assertEqual(cm.exception.__str__(), "No work in node a")

    def test_work_node_must_have_work(self):
        with self.assertRaises(VerifyError) as cm:
            self.check({
                'id': 'a',
                'class': 'WorkNode',
            })

        self.assertEqual(cm.exception.__str__(), "No work in node a")
