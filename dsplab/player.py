# Copyright (C) 2017-2021 Aleksandr Popov, Kirill Butin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Playing signal from file. Online mode for offline data."""

import threading
from threading import Lock, Event
from collections import deque
import time
import random
import logging

LOG = logging.getLogger(__name__)


class RepeatedTimer:
    """Timer."""
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self._interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = None
        self.lock = Lock()

    def set_interval(self, interval):
        """Set interval."""
        self._interval = interval

    def get_interval(self):
        """Get interval."""
        return self._interval

    interval = property(get_interval, set_interval,
                        doc="Timeout interval (sec)")

    def start(self):
        """Start timer."""
        self.next_call = time.time()
        self.is_running = True
        self._repeat()

    def stop(self):
        """Stop timer."""
        self._timer.cancel()
        self.is_running = False

    def _repeat(self):
        # LOG.debug("%s._repeat" % self.__class__.__name__)
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
    """Class for playing text file as stream."""
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
        # LOG.debug('call SignalPlayer.start()')
        self.new_data_ready.clear()
        self.timer.set_interval(self.interval)
        self.data_producer.start()
        self.timer.start()

    def stop(self):
        """Stop player."""
        # LOG.debug("%s.stop()" % self.__class__.__name__)
        self.timer.stop()
        self.data_producer.stop()

    def _produce_data(self):
        # LOG.debug("%s._produce_data()" % self.__class__.__name__)
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
        sample = random.randint(*self.interval)
        return sample


class CsvDataProducer(DataProducer):
    """Produces sample from headered CSV file."""
    def __init__(self, file_name=None, delimiter=';',
                 encoding='utf-8', columns=None):
        self.file_name = file_name
        self.encoding = encoding
        self._delimiter = None
        self.set_delimiter(delimiter)
        self._keys = None
        if columns is not None:
            self.select_columns(columns)
        self._headers = None
        self._indexes = None
        self._lines = None

    def set_delimiter(self, delimiter):
        """Set delimiter."""
        self._delimiter = delimiter

    def get_delimiter(self):
        """Return delimiter."""
        return self._delimiter

    delimiter = property(get_delimiter, set_delimiter,
                         doc="delimiter in CSV file.")

    def set_file(self, file_name, delimiter=None, encoding='utf-8'):
        """Set file for reading."""
        self.file_name = file_name
        if delimiter is not None:
            self.set_delimiter(delimiter)
        self.encoding = encoding

    def select_columns(self, keys):
        """Select returned columns. Numbers or names of columns can be
        used."""
        self._keys = keys

    def _detect_indexes(self):
        """Detect indexes of selected columns."""
        if isinstance(self._keys[0], int):
            self._indexes = self._keys
        else:
            indexes = []
            for key in self._keys:
                try:
                    index = self._headers.index(key)
                    indexes.append(index)
                except ValueError:
                    pass
            self._indexes = indexes

    def start(self):
        """Init reader."""
        # LOG.debug('Call CsvDataProducer.start()')
        with open(self.file_name, encoding=self.encoding) as buf:
            self._lines = iter(buf.read().split('\n'))
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
            sample = ['' for ind in self._indexes]
        except IndexError:
            sample = ['' for ind in self._indexes]
        return sample
