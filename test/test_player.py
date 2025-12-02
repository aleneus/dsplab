from unittest import TestCase
from dsplab import player


class TestRepeatedTimer(TestCase):

    def test_set_get_interval(self):
        timer = player.RepeatedTimer(2, lambda x: x)
        timer.interval = 1

        self.assertEqual(timer.interval, 1)

    def test_start_stop_with_args(self):
        timer = player.RepeatedTimer(1, lambda x: x, [1])

        timer.start()
        timer.stop()

    def test_start_stop_no_args(self):
        timer = player.RepeatedTimer(1, lambda: None)

        timer.start()
        timer.stop()

    def test_stop_before_start(self):
        timer = player.RepeatedTimer(1, lambda: None)

        timer.stop()


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
