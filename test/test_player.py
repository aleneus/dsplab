from unittest import TestCase
from dsplab import player


class TestRepeatedTimer(TestCase):
    def test_touch(self):
        player.RepeatedTimer(1, lambda x: x)


class TestSignalPlayer(TestCase):
    def test_touch(self):
        player.SignalPlayer(1)


class TestDataProducer(TestCase):
    def test_touch(self):
        player.DataProducer()


class TestRandomDataProducer(TestCase):
    def test_touch(self):
        player.RandomDataProducer(1)


class TestCsvDataProducer(TestCase):
    def test_touch(self):
        player.CsvDataProducer()
