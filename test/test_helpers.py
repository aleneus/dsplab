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
