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
from dsplab.flow.activity import (Activity, Work, get_work_from_dict)


class TestActivity(unittest.TestCase):
    def test_class_info(self):
        a = Activity()
        info = a.class_info()
        self.assertEqual(len(info), 2)
        self.assertTrue('class' in info)

    def test_set_call(self):
        a = Activity()
        raised = False
        try:
            a(1)
        except NotImplementedError:
            raised = True

        self.assertTrue(raised)


class TestWork(unittest.TestCase):
    def test_inc(self):
        w = Work()
        w.set_worker(lambda x: x + 1)
        r = w(1)
        self.assertEqual(r, 2)

    def test_change_worker(self):
        w = Work()
        w.set_worker(lambda x: x + 1)
        w.set_worker(lambda x: x + 2)
        self.assertEqual(w(1), 3)

    def test_no_worker(self):
        w = Work()
        raised = False
        try:
            w(1)
        except TypeError:
            raised = True

        self.assertTrue(raised)


class Test_get_from_dict(unittest.TestCase):
    def test_no_worker(self):
        with self.assertRaises(RuntimeError):
            get_work_from_dict({})

    def test_descr_not_empty(self):
        settings = {
            'descr': 'My work',
            'worker': {
                'function': 'test.test_flow.test_activity.inc',
            }
        }
        self.assertEqual(get_work_from_dict(settings).descr, 'My work')

    def test_descr_empty(self):
        settings = {
            'worker': {
                'function': 'test.test_flow.test_activity.inc',
            }
        }
        self.assertEqual(get_work_from_dict(settings).descr, '')

    def test_wrong_worker(self):
        settings = {
            'worker': {
                'procedure': 'test.test_flow.test_activity.inc',
            }
        }
        with self.assertRaises(RuntimeError):
            get_work_from_dict(settings)

    def test_worker_is_function(self):
        settings = {
            'worker': {
                'function': 'test.test_flow.test_activity.inc',
            }
        }
        self.assertEqual(get_work_from_dict(settings)(1), 2)

    def test_worker_is_class(self):
        settings = {
            'worker': {
                'class': 'test.test_flow.test_activity.Inc',
                'params': {'val': 2},
            }
        }
        self.assertEqual(get_work_from_dict(settings)(1), 3)

    def test_variable_params(self):
        settings = {
            'worker': {
                'class': 'test.test_flow.test_activity.Inc',
                'params': {'val': '$var'},
            }
        }
        w = get_work_from_dict(settings, params={'var': 2})
        self.assertEqual(w(1), 3)

        w = get_work_from_dict(settings, params={'var': 3})
        self.assertEqual(w(1), 4)

    def test_combination_constant_and_variable_parameters(self):
        settings = {
            'worker': {
                'class': 'test.test_flow.test_activity.Lin',
                'params': {'a': '$a', 'b': 0},
            }
        }
        w = get_work_from_dict(settings, params={'a': 2})
        self.assertEqual(w(1), 2)

        w = get_work_from_dict(settings, params={'a': 3})
        self.assertEqual(w(2), 6)


def inc(x):
    return x + 1


class Inc:
    def __init__(self, val):
        self.val = val

    def __call__(self, x):
        return x + self.val


class Lin:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, x):
        return self.a * x + self.b
