"""Playing signal from file: online mode for offline data."""

import threading
from threading import Lock, Event
from collections import deque
import time
import random


class SignalPlayer:
    """Playing the text file as stream."""

    def __init__(self, interval):
        self.interval = interval
        self.queue = deque([], maxlen=100)
        self.timer = RepeatedTimer(interval, self._produce_data)
        self.new_data_ready = Event()
        self.lock = Lock()
        self.data_producer = None

    def set_data_producer(self, data_producer):
        """Set adapter with get_sample() method."""
        self.data_producer = data_producer

    def start(self):
        """Start player."""
        self.new_data_ready.clear()
        self.timer.interval = self.interval
        self.data_producer.start()
        self.timer.start()

    def stop(self):
        """Stop player."""
        self.timer.stop()
        self.data_producer.stop()

    def _produce_data(self):
        with self.lock:
            sample = self.data_producer.get_sample()

        self.queue.append(sample)
        self.new_data_ready.set()

        return sample

    def get_sample(self):
        """Return sample."""
        try:
            sample = self.queue.popleft()
        except IndexError:
            self.new_data_ready.clear()
            self.new_data_ready.wait()
            sample = self.queue.popleft()

        return sample


class DataProducer:
    """Base class for adapters for data producer."""

    def get_sample(self):
        """Return sample."""
        raise NotImplementedError

    def start(self):
        """Do some operations in producer when player starts."""

    def stop(self):
        """Do some operations in producer when player stops."""


class RandomDataProducer(DataProducer):
    """Data producer with random values on output."""

    def __init__(self, interval):
        self.interval = interval

    def get_sample(self):
        """Return sample."""
        return random.randint(*self.interval)


class CsvDataProducer(DataProducer):
    """Produces sample from headered CSV file."""

    def __init__(self,
                 file_name=None,
                 delimiter=";",
                 encoding="utf-8",
                 columns=None):
        self.file_name = file_name
        self.encoding = encoding

        self.set_delimiter(delimiter)

        self._keys = None
        self._headers = None
        self._indexes = None
        self._lines = None

        if columns is not None:
            self.select_columns(columns)

    def set_delimiter(self, delimiter):
        """Set delimiter."""
        self._delimiter = delimiter

    def get_delimiter(self):
        """Return delimiter."""
        return self._delimiter

    delimiter = property(get_delimiter,
                         set_delimiter,
                         doc="delimiter in CSV file.")

    def set_file(self, file_name, delimiter=None, encoding="utf-8"):
        """Set file for reading."""
        self.file_name = file_name
        self.encoding = encoding

        if delimiter is not None:
            self.set_delimiter(delimiter)

    def select_columns(self, keys):
        """Select returned columns, numbers or names of columns can be used."""
        self._keys = keys

    def _detect_indexes(self):
        """Detect indexes of selected columns."""
        if isinstance(self._keys[0], int):
            self._indexes = self._keys

            return

        indexes = []
        for key in self._keys:
            try:
                indexes.append(self._headers.index(key))
            except ValueError:
                pass

        self._indexes = indexes

    def start(self):
        """Init reader."""
        with open(self.file_name, encoding=self.encoding) as buf:
            self._lines = iter(buf.read().split("\n"))

        line = next(self._lines)
        self._headers = line.split(self._delimiter)
        self._detect_indexes()

    def get_sample(self):
        """Return sample."""
        sample = []

        try:
            line = next(self._lines)
            full_sample = line.split(self._delimiter)

            if self._indexes is None:
                return full_sample

            for ind in self._indexes:
                sample.append(full_sample[ind])

        except StopIteration:
            sample = ["" for ind in self._indexes]

        except IndexError:
            sample = ["" for ind in self._indexes]

        return sample


class RepeatedTimer:
    """Timer which calls the given function each interval."""

    def __init__(self, interval, func, *args, **kwargs):
        self._timer = None
        self._interval = interval
        self._func = _Func(func, *args, **kwargs)
        self._is_running = False
        self._next_call = None
        self._lock = Lock()

    @property
    def interval(self):
        """Return current interval, sec."""
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Set repeat interval, sec."""
        self._interval = interval

    def start(self):
        """Start timer."""
        self._next_call = time.time()
        self._is_running = True
        self._repeat()

    def stop(self):
        """Stop timer."""
        if not self._is_running:
            return

        self._timer.cancel()

        self._is_running = False

    def _repeat(self):
        if not self._is_running:
            return

        with self._lock:
            self._next_call += self._interval

            self._timer = threading.Timer(
                self._next_call - time.time(),
                self._repeat,
            )

            self._timer.start()

        self._func()


class _Func:
    # pylint: disable=too-few-public-methods

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        self._func(*self._args, **self._kwargs)
