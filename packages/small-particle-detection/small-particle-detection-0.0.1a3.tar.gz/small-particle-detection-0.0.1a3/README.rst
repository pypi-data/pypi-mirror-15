Small Particle Detection
========================

An algorithm primarily design to detect objects whose sizes aren't larger a
few pixels (particles) on fluorescence microscopy images.

It is an simplified version of marked point process.


Requirements
============
SPADE has only been tested with Python 3.5 but should work with older versions.
The only other requirement is Numpy.
In order to use SPADE to its full extent, we recommend installing the
scikit-image package and the full scipy ecosystem.


Usage
=====

You can install the package using PIP. The main function, spade2d, is in the
spade.detection_2d module. It takes an image, a shapes library and a
threshold as input. See the examples in the example folder for more
information.

Also provided is a command line interface, that can be used as following:

::

    python -m spade.cli

Launch this command with -h for more information on its usage.

Take a look at the 'example' to see how to use SPADE from within a python
script.