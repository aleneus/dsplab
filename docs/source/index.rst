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

What's new in 0.26
------------------

* Modulation: Return angles from fm()
* Activity: Add a function for setup work from dictionary
* Plan: Add a function for setup plan from dictionary
* Plan: Deprecate setup_plan()
* Plan: Update demo
* Modulation: Add a function for generate the harmonic signal (with constant amplitude, frequency and phase)

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
