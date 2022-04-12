from unittest import TestCase
from dsplab.flow import online


class TestQueueFilter(TestCase):
    def test_touch(self):
        online.QueueFilter(101)


class TestDelayer(TestCase):
    def test_touch(self):
        online.Delayer(101)


class TestAnd(TestCase):
    def test_touch(self):
        online.And()


class TestOr(TestCase):
    def test_touch(self):
        online.Or()


class TestOnlineFilter(TestCase):
    def test_touch(self):
        online.OnlineFilter()
