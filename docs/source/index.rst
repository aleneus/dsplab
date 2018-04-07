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

What's new in 0.25
------------------

* Modulation: Add noise_a and noise_f parameters to am, fm, phm
* Plan: Add the key 'function' to explicit description of worker in node settings
* Plan: Add a worker with no init args to the example of setup_plan
* Docs: Add more examples
* Some bugs fixed

Modules
-------

DSP procedures
^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   modulation
   filtration
   frequency
   envelope
   prony
   spectran

Ornanization of calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   activity
   plan
	      
History
-------   
   
.. toctree::
   :maxdepth: 1

   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
