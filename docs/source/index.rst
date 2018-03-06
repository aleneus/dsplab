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

What's new in 0.19
------------------

* Activity module redesigned.
* Info stuff of activities redesigned.
* Work class added. Work is the activity that can be done by different
  ways. Work has worker. Wroker is the activity.
* Added tools for constructing the plans of works. Plan is the number
  of linked nodes and every node is the 'work place' for some worker.

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
   :maxdepth: 2

   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
