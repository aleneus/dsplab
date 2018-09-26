# dsplab package

## Fields of application

* Development of software for digital signal processing.
* Investigation of variety of methods solving the same DSP task.
* Development of the DSP routines that require a flexible configuration of different stages of calculations on the user level.

## Features and characteristics

* Some specific functions for analysis of signals.
* Synthesis of test signals with different kinds of **modulation**: amplitude, frequency and phase.
* **Playing** of signals (synthesized or archive) for the development of on-line procedures.
* Organization of calculations, **workflows**:
    - User can define the **plan of works** and then set the **worker** for every work. The replacement of the worker does not destroy the workflow.
    - Different types of nodes are supported: **Work**, **Map (Loop)**, **Select** and **Pack**.
    - Base classes for workers are defined. Every worker can return detailed description of itself by calling **info()** method.
    - Base class for on-line filters having **add_sample()** method and embedded **queues** for running window and smoothing of results is implemented.
* Licence: **LGPLv3**
* Programming language: **Python 3**.

## Documentation

http://dsplab.readthedocs.io/en/latest/

