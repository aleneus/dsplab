# Copyright (C) 2017-2022 Aleksandr Popov
# Copyright (C) 2021-2022 Kirill Butin

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

import numpy as np


def harmonic(T, fs, f, A=1, phi=0):
    """Generate harmonis signal."""
    t = np.linspace(0, T, T*fs + 1)
    x = A * np.cos(2 * np.pi * f * t + phi)

    return x, t
