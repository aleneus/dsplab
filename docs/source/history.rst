0.26
====

* Modulation: Return angles from fm()
* Activity: Add a function for setup work from dictionary
* Plan: Add a function for setup plan from dictionary
* Plan: Deprecate setup_plan()
* Plan: Update demo
* Modulation: Add a function for generate the harmonic signal (with constant amplitude, frequency and phase)

0.25
====

* Modulation: Add noise_a and noise_f parameters to am, fm, phm
* Plan: Add the key 'function' to explicit description of worker in node settings
* Plan: Add a worker with no init args to the example of setup_plan
* Docs: Add more examples
* Some bugs fixed

0.24
====

* Plan: Provide auto and manual terminals without auto_terminals option
* Plan: Support the inputs and ouputs in the function for setup plan from dict 
* Plan: Rename Translator to Transmitter
* Modulation: Add a function for phase modulation

0.23
====

* Activity: Remove Strategy and subclasses
* Activity: Use the docstring for description in _info
* Plan: Add docstrings to Plan.outputs property
* Plan: Add remove node method and demo
* Plan: Remove detection of terminals from call
* Plan: Add auto_terminals option to init
* Demo: Replace plan examples to plan/ folder from activity/
* Add link to docs to README

0.22
====

* Restructure todo
* Add function am to modulation unit
* Add function fm to modulation unit
* Add demo for am
* Add demo for fm

0.21
====

* The possibility of specifying outputs is supported.
* The Translator node is added for constructing more flexible input of plan.
* More examples of using plans are added.
* The hooks for starting and finishing calculations in node are added.
* A small refactoring is performed.

0.20
====

* The function for setup plan. The settings are taken from list of dictionaries.
* Refactoring.

0.19
====

* Activity module redesigned.
* Info stuff of activities redesigned.
* Work class added. Work is the activity that can be done by different
  ways. Work has worker. Wroker is the activity.
* Added tools for constructing the plans of works. Plan is the number
  of linked nodes and every node is the 'work place' for some worker.

0.18
====

* The module activity containing base classes for different processing tools added.


0.17
====

* The base class for online filters was added

0.16
====

* Add digital_hilbert_filter function to envelope and deprecate hilbert_filter
* Add example for IQ demodulation

0.15
====

* More universal function for QI-processing was added.

0.14
====

* Window parameter was added to spectrum and stft.
* Some code in spectran enhanced.

0.13
====
* Function for calculation of frequency using wave lengths was added.
* Fixed errors in spectrogram calculation.

0.12
====

* Function for calculation of instantaneous frequency with phasor was added to new module called modulation.
* Function for calculation of spectrogram was added.
* Function for finding the trend with smoothing filtration was added.
* Stupid filters (FFT and back) were added.
* Spectrum function was rewrited.
* Some code was cleaned.
* More tests were added.

0.11
====

* Function for calculation of order of Butterworth bandpass filter was added.
* Some docs were added.

0.10
====

* Tools for spectral analysis were added
* Haar transform was added
* More demos were added
* Some bugs were fixed

0.9
===

* Function for calculation digital Hilbert filter was added 
* Demo for digital Hilbert filter was added

0.8
===

* Specfic module damping was removed
* Function for read signal from csv was added
* More tests were added

0.7
===

* Envelope by maximums replaced to envelope by extremums.
* Demos added.
* More tests added.


0.6
===

* Prony's decomposition of signal is added.


0.5
===

* Stupid procedure for calculationg damping time is added.
