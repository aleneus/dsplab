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

What's new in 0.38
------------------

* Activity methods **info()** and **set_descr()** have been marked as deprecated
* **Worker** class has been marked as deprecated
* New Node's method **get_result_info()**
* New Plan's property **descr**
* **reset()** method of the Node has been renamed to **clear_result()**

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
   run-demo


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
