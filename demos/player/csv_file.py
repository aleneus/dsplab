import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from dsplab.player import CsvDataProducer, SignalPlayer

def main():
    """ Example of playing signal. """
    data_producer = CsvDataProducer()
    data_producer.set_delimiter(',')
    data_producer.open_file("test.csv")
    data_producer.select_columns(['F', 'Ua1'])
    # data_producer.select_columns([0, 1]) # <--- It's all right too
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
