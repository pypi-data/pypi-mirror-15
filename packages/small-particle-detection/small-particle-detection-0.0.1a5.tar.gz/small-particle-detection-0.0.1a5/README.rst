SPADE: Small Particle Detection
===============================

.. image:: http://www-sop.inria.fr/morpheme/images/logo2.png
   :width: 200 px
   :target: http://www-sop.inria.fr/morpheme/team.html

An algorithm primarily design to detect objects whose sizes aren't larger a
few pixels (particles) on fluorescence microscopy images.

It is an simplified version of marked point process.


Requirements
============
SPADE has only been tested with Python 3.5 but should work with older versions.
The only strict requirement is the package `numpy`.
In order to use SPADE to its full extent, we recommend installing the
`scikit-image` package and the full `scipy` ecosystem.


Usage
=====

You can install the package using PIP. The main function, `spade2d`, is in the
`spade.detection_2d` module. It takes an image, a shapes library and a
threshold as input. See the examples in the example folder for more
information.

Also provided is a command line interface, that can be used as following:

::

    python -m spade.cli INPUT_IMAGE THRESHOLD -o /path/to/output_image.png

Launch this command with `-h` for more information on its usage.

Take a look at the files in the `example` folder to see how to use SPADE from
within a python script.


Authors & Acknowledgments
=========================


SPADE was developed by `Nicolas Cedilnik
<mailto:nicoco@nicoco.fr>`_, `Éric Debreuve
<http://www.i3s.unice.fr/~debreuve/>`_ and `Xavier Descombes
<http://www-sop.inria.fr/members/Xavier.Descombes/>`_ at the `MORPHEME team
<http://www-sop.inria.fr/morpheme/team.html>`_.

If you use SPADE for your scientific work, please include this `bibtex` (or
equivalent) entry:

::

    @misc{descombes2016spade,
      title={SPADE: Small particle detection}
      author={Cedilnik, Nicolas and Debreuve, Éric and Descombes, Xavier}
      url={https://pypi.python.org/pypi/small-particle-detection}
      year={2016}
    }

License
=======
SPADE is released under the `CeCILL-2.1 licence
<http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.txt>`_.
