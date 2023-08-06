positronium
===========

python tools pertaining to positronium

Prerequisites
-------------

Tested using Anaconda (Continuum Analytics) with Python 2.7 and 3.5.
Examples written using IPython 4.0.1 (python 3.5.1 kernel).

Package dependencies:

-  scipy, numpy

IPython examples dependencies:

-  matplotlib

Installation
------------

via pip (recommended):

::

    pip install positronium

alternatively, try the development version

::

    git clone https://github.com/PositroniumSpectroscopy/positronium

and then run

::

    python setup.py install

About
-----

This package is designed to collate useful bits of code relating to the
positronium atom (an electron bound to its antiparticle, the positron).
The functions are generally simple approximations that give roughly the
right answers, rather than rigorous quantum mechanical calculations.

The package currently only contains a few very simple modules.

constants
~~~~~~~~~

is intended to collect useful constants in SI units, including:

+-------------------+-----------------------------------------------------------+
| const             | description                                               |
+===================+===========================================================+
| m\_Ps             | 2 \* mass\_electron                                       |
+-------------------+-----------------------------------------------------------+
| Rydberg\_Ps       | Rydberg value for Ps                                      |
+-------------------+-----------------------------------------------------------+
| a\_Ps             | Bohr radius for Ps                                        |
+-------------------+-----------------------------------------------------------+
| decay\_pPs        | decay rate of para-Ps (S=0)                               |
+-------------------+-----------------------------------------------------------+
| decay\_oPs        | decay rate of ortho-Ps (S=1)                              |
+-------------------+-----------------------------------------------------------+
| lifetime\_pPs     | lifetime of para-Ps (S=0)                                 |
+-------------------+-----------------------------------------------------------+
| lifetime\_oPs     | lifetime of ortho-Ps (S=1)                                |
+-------------------+-----------------------------------------------------------+
| frequency\_hfs    | frequency of the ground-state hyperfine splitting         |
+-------------------+-----------------------------------------------------------+
| energy\_hfs       | energy interval of the ground-state hyperfine splitting   |
+-------------------+-----------------------------------------------------------+
| frequency\_1s2s   | frequency of the 1s2s transition                          |
+-------------------+-----------------------------------------------------------+
| energy\_1s2s      | energy interval of the 1s2s transition                    |
+-------------------+-----------------------------------------------------------+

Example usage,

.. code:: python

    >>> from positronium.constants import lifetime_oPs, frequency_hfs
    >>> print("The mean lifetime of ortho-Ps is", "%.1f ns."%(lifetime_oPs * 1e9))
    The mean lifetime of ortho-Ps is 142.0 ns.

    >>> print("The ground-state hyperfine splitting is", "%.1f GHz."%(frequency_hfs * 1e-9))
    The ground-state hyperfine splitting is 203.4 GHz.

Where appropriate constants are stored in a subclass of float called
MeasuredValue, which has a few extra attributes [uncertainty, unit,
source, url], for example

.. code:: python

    >>> lifetime_oPs
    1.4203738423953184e-07

    >>> lifetime_oPs.uncertainty
    3.631431333889514e-11

    >>> print(lifetime_oPs.source)
    R. S. Vallery, P. W. Zitzewitz, and D. W. Gidley (2003) Phys. Rev. Lett. 90, 203402

    >>> lifetime_oPs.article()

The final line opens a url to the source journal.

Bohr
~~~~

contains an adaptation of the Rydberg formula, which is used to
calculate the principle energy levels of positronium, or the interval
between two levels. The default unit is 'eV', however, this can be
changed using the keyword argument 'unit'.

For instance, the UV wavelength (in nm) needed to excite the Lyman-alpha
transition can be found by:

.. code:: python

    >>> from positronium import Bohr
    >>> Bohr.energy(1, 2, unit='nm')
    243.00454681357735

This accepts numpy arrays for the initial (n1) and/ or final (n2) energy
level, e.g.,

.. code:: python

    >>> import numpy as np
    >>> n1 = np.arange(1, 10)
    >>> np.array([n1, Bohr.energy(n1, unit='eV')]).T
    array([[ 1.        ,  6.8028465 ],
           [ 2.        ,  1.70071163],
           [ 3.        ,  0.75587183],
           [ 4.        ,  0.42517791],
           [ 5.        ,  0.27211386],
           [ 6.        ,  0.18896796],
           [ 7.        ,  0.1388336 ],
           [ 8.        ,  0.10629448],
           [ 9.        ,  0.08398576]])

Ps
~~

This package contains a class called Ps, which can be used to represent a
particular atomic state of positronium using the quantum numbers

+-----+----------------------------+
| n   | principle                  |
+-----+----------------------------+
| l   | orbital angular momentum   |
+-----+----------------------------+
| m   | magnetic quantum number    |
+-----+----------------------------+
| S   | total spin                 |
+-----+----------------------------+
| J   | total angular momentum     |
+-----+----------------------------+

This can be used to return estimates of, e.g., the energy
level,

.. code:: python

    >>> from positronium import Ps
    >>> x1 = Ps(n=2, l=1, S=1, J=2)
    >>> x1.energy(unit='eV')
    -1.7007156827724967

which uses an equation described in

    Richard A. Ferrell (1951) Phys. Rev. 84, 858
    http://dx.doi.org/10.1103/PhysRev.84.858

This includes fine structure but not radiative corrections.

A representation of the state using Latex code can be made using,

.. code:: python

    >>> x1.tex()
    '$2^{3}P_{2}$'

For further examples see the IPython/ Jupyter notebooks,

https://github.com/PositroniumSpectroscopy/positronium/tree/master/examples
