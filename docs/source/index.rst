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

What's new in 0.32
------------------

* Add new types of nodes: WorkNode, MapNode, PackNode and SelectNode
* Update get_plan_from_dict() to support all types of nodes
* Update examples
* Add get_nodes() to Plan
* Support progress handling in plan
* Add arguments to hooks of nodes
* Refactoring of plan.py    

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
