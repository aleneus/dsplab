activity
========

.. automodule:: dsplab.flow.activity
   :members:
   :undoc-members:
   :show-inheritance:


online
======

.. automodule:: dsplab.flow.online
   :members:
   :undoc-members:
   :show-inheritance:


plan
====

Examples
--------

Helper module with workers
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/workers.py
   :language: python

Basic usage
~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/basic.py
   :language: python

Using of start and stop hooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/hooks.py
   :language: python

MapNode (applying work for iterable input)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/map.py
   :language: python

PackNode (pack inputs to list)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/pack.py
   :language: python

SelectNode
~~~~~~~~~~

.. literalinclude:: ../../demo/flow/select.py
   :language: python

Node-generator
~~~~~~~~~~~~~~

'Node-generator' means the no input node with no inputs.

.. literalinclude:: ../../demo/flow/generator.py
   :language: python

Get Plan instance from dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/get_plan_from_dict.py
   :language: python

Quick plan for on-line processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../demo/flow/online.py
   :language: python

Members
-------

.. automodule:: dsplab.flow.plan
   :members:
   :undoc-members:
   :show-inheritance:

Verification
------------

.. automodule:: dsplab.flow.verify
   :members:
   :undoc-members:
   :show-inheritance:
