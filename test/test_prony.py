import unittest
from dsplab.prony import prony_decomp


class TestProny(unittest.TestCase):

    def test_prony_sum_length_of_result(self):
        x = [
            255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2,
            -2, 1, -1, 0, 0
        ]
        L = 4
        ms, cs, es = prony_decomp(x, L)
        self.assertEqual(len(ms) + len(cs) + len(es), 4 + 4 + 4)

    def test_prony_length_of_components(self):
        x = [
            255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2,
            -2, 1, -1, 0, 0
        ]
        L = 4
        ms, cs, es = prony_decomp(x, L)
        self.assertEqual(len(es[0]), len(x))

    def test_prony_wrong_number_of_components(self):
        x = [
            255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2,
            -2, 1, -1, 0, 0
        ]
        L = len(x) // 2 + 1
        res = prony_decomp(x, L)
        self.assertEqual(res, None)

    def test_prony_double_number_of_components_equal_to_n(self):
        x = [
            255, -255, 128, -128, 64, -64, 32, -32, 16, -16, 8, -8, 4, -4, 2,
            -2, 1, -1, 0, 0
        ]
        L = 10
        ms, cs, es = prony_decomp(x, L)
        self.assertEqual(len(ms) + len(cs) + len(es), 10 + 10 + 10)
