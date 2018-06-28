""" Playing signal from file. Online mode for offline data. """

import threading
from threading import Lock, Event
from collections import deque
import time
import random
import csv

__all__ = ["RepeatedTimer", "SignalPlayer", "DataProducer",
           "RandomDataProducer", "CsvDataProducer"]


class RepeatedTimer(object):
    """ Timer. """
    def __init__(self, interval, function, *args, **kwargs):
        """ Initialization. """
        self._timer = None
        self._interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = None
        self.lock = Lock()

    def set_interval(self, interval):
        """ Set interval. """
        self._interval = interval

    def get_interval(self, interval):
        """ Get interval. """
        return self._interval

    interval = property(get_interval, set_interval, doc="Timeout interval (sec)")

    def start(self):
        """ Start timer. """
        self.next_call = time.time()
        self.is_running = True
        self._repeat()

    def stop(self):
        """ Stop timer. """
        self._timer.cancel()
        self.is_running = False
        
    def _repeat(self):
        if not self.is_running:
            return
        with self.lock:
            self.next_call += self._interval
            self._timer = threading.Timer(
                    self.next_call - time.time(),
                    self._repeat
                )
            self._timer.start()
        self.function(*self.args, **self.kwargs)


class SignalPlayer:
    """ Class for playing text file as stream. """
    def __init__(self, interval):
        """ Initialization. """
        self.interval = interval
        self.queue = deque([], maxlen=100)
        self.timer = RepeatedTimer(interval, self._produce_data)
        self.new_data_ready = Event()
        self.lock = Lock()
        self.data_producer = None

    def set_data_producer(self, data_producer):
        """ Set adapter with get_sample() method. """
        self.data_producer = data_producer

    def start(self):
        """ Start player. """
        self.queue.clear()
        self.new_data_ready.clear()
        self.timer.set_interval(self.interval)
        self.timer.start()

    def stop(self):
        """ Stop player. """
        self.timer.stop()

    def _produce_data(self):
        with self.lock:
            sample = self.data_producer.get_sample()
        self.queue.append(sample)
        self.new_data_ready.set()
        return sample

    def get_sample(self):
        """ Return sample. """
        try:
            sample = self.queue.popleft()
        except IndexError:
            self.new_data_ready.clear()
            self.new_data_ready.wait()
            sample = self.queue.popleft()
        return sample


class DataProducer:
    """ Base class for adapters for data producer. """
    def get_sample(self):
        """ Return sample. """
        raise NotImplementedError


class RandomDataProducer(DataProducer):
    """ Data producer with random values on output. """
    def __init__(self, interval):
        self.interval = interval

    def get_sample(self):
        """ Return sample. """
        sample = random.randint(*self.interval)
        return sample


class CsvDataProducer(DataProducer):
    """ Produces sample from headered CSV file. """
    def __init__(self):
        self.csv_reader = None
        self.file_buffer = None
        self.headers = None
        self.indexes = None
        self.delimiter = ';'

    def set_delimiter(self, delimiter):
        """ Set delimiter. """
        self.delimiter = delimiter

    def _reset(self):
        try:
            self.file_buffer.close()
        except AttributeError:
            pass
        finally:
            pass
        self.headers = None
        self.indexes = None

    def open_file(self, file_name, delimiter=None, encoding='utf-8'):
        """ Set input file. """
        self._reset()
        if delimiter is not None:
            self.delimiter = delimiter
        self.file_buffer = open(file_name, encoding=encoding)
        self.csv_reader = csv.reader(
            self.file_buffer,
            delimiter=self.delimiter
        )
        self.headers = next(self.csv_reader)

    def close_file(self):
        """ Close input file. """
        self._reset()

    def select_columns(self, keys):
        """ Select returned columns, key_type can be 'name' or
        'index'. """
        if isinstance(keys[0], int):
            self.indexes = keys
        else:
            indexes = []
            for key in keys:
                try:
                    index = self.headers.index(key)
                    indexes.append(index)
                except ValueError:
                    pass
            self.indexes = indexes

    def get_sample(self):
        """ Return sample. """
        sample = []
        try:
            full_sample = next(self.csv_reader)
            if self.indexes is None:
                return full_sample
            for ind in self.indexes:
                sample.append(full_sample[ind])
        except StopIteration:
            sample = ['' for ind in self.indexes]
        return sample
