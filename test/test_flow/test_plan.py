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
