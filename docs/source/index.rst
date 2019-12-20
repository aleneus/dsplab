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

* Deprecate info() in activities
* Deprecate Worker class (just use Activity)
* Add Node.get_result_info()
* Deprecate Activity.set_descr()
* Add Work.set_descr()
* Add tests
* Update examples
* Add Plan.descr property
* Rename Node.reset() to Node.clear_result(). Deprecate reset().

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
