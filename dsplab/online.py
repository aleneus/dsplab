# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
