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

What's new in 0.23
------------------

* Activity: Remove Strategy and subclasses
* Activity: Use the docstring for description in _info
* Plan: Add docstrings to Plan.outputs property
* Plan: Add remove node method and demo
* Plan: Remove detection of terminals from call
* Plan: Add auto_terminals option to init
* Demo: Replace plan examples to plan/ folder from activity/
* Add link to docs to README

Modules
-------

.. toctree::
   :maxdepth: 2

   activity
   plan
   modulation
   frequency
   envelope
   prony
   spectran
   filtration

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
