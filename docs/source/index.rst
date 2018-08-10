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

What's new in 0.28
------------------

* Add class info of Activity in metaclass
* Add method for getting information about class of Activity whithout creating instance
* Add method for adding and documenting parameters of activity
* Brush activity module with pylint
* Some fixes

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

Organization of calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   activity
   plan

Online processing
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   player
	      
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
