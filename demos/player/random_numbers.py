""" Example of playing random signal. """

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

from dsplab.player import RandomDataProducer, SignalPlayer

def main():
    """ Entry point. """
    data_producer = RandomDataProducer(interval=(1, 100))
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
