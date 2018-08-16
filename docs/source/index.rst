.. dsplab documentation master file, created by
   sphinx-quickstart on Mon Oct  2 17:03:30 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dsplab's documentation!
==================================

Digital signal processing tools

.. toctree:
   :maxdepth: 2
   :caption: Contents:

Requirements
------------

* numpy
* scipy

What's new in 0.30
------------------

* Add descr option to __init__ of Plan
* Add function for simultaneous amp and freq modulation
* Brush modulation module
* Rename functions names and arguments in modulation unit
* Set default phi=0 in modulation
* Merge envelop module to modulation one
* Update envelop examples
* Update modulation examples
* Refactoring iq_demod()

Modules
-------

DSP procedures
^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   modulation
   filtration
   prony
   spectran

Organization of calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   activity
   plan
   online

Online processing
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   player
	      
Project
-------   
   
.. toctree::
   :maxdepth: 1

   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
