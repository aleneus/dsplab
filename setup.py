# Copyright (C) 2017-2021 Aleksandr Popov
# Copyright (C) 2021 Kirill Butin

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

""" Dsplab is the package for building generalized signal processing schemes.

In a different subject areas, data analysis tasks exist in which a
certain general structure is distinguished, while the number of
possible methods for implementing subtasks increases. The question
arises: which combination of methods is better? Dsplab allows you to
describe the overall scheme of the task (plan) and assign the
so-called "workers" to perform the subtasks. So the main field of
application of dsplab is the investigation of variety of methods
solving the same signal processing task.

"""

import os
from setuptools import setup
from dsplab import __version__


DOCLINES = __doc__.split("\n")


def read(fname):
    """Read content of the text file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


INSTALL_REQUIRES = [
    'numpy>=1.14',
    'scipy>=0.19',
    'jsonschema>=3.2',
]


PACKAGES = [
    'dsplab',
    'dsplab.flow',
]


PACKAGE_DATA = {
    'dsplab': [
        'data/*',
    ],
}


setup(
    name='dsplab',
    version=__version__,
    description=DOCLINES[0],
    author="Aleksandr Popov, Kirill Butin",
    author_email="aleneus@gmail.com",
    license="LGPLv3",
    keywords="digital signal processing",
    url="https://github.com/aleneus/dsplab",
    long_description="\n".join(DOCLINES[2:]),
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
