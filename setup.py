"""Setup script."""

from setuptools import setup
from dsplab import __version__

DOCLINES = __doc__.split("\n")

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
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
