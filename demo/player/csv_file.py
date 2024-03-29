"""Example of playing signal from CSV file."""
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

# pylint: disable=wrong-import-position
from dsplab.player import CsvDataProducer, SignalPlayer


def main():
    """Play CSV file."""
    data_producer = CsvDataProducer(file_name="demo/player/test.csv",
                                    delimiter=',')
    data_producer.select_columns(['F', 'Ua1'])

    # Next would be right too
    # data_producer.select_columns([0, 1])

    player = SignalPlayer(interval=0.02)
    player.set_data_producer(data_producer)

    player.start()

    while True:
        try:
            sample = player.get_sample()
            print(sample)
        except KeyboardInterrupt:
            break

    player.stop()


if __name__ == "__main__":
    main()
