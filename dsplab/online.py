""" This module implements the base class for online filters. """

import numpy as np
from collections import deque

# Compatibility
from dsplab.activity import OnlineFilter # TODO: remove in new version

pi = 3.141592653589793
pi2 = 2*pi

def unwrap_point(w):
    """ Unwrap angle (for signle value). """
    if w < -pi:
        return w + pi2
    if w > pi:
        return w - pi2
    return w
