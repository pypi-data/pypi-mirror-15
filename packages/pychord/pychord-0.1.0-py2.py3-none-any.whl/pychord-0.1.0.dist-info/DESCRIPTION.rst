pychord
=======

|Build Status|

Overview
--------

Pychord is a python library to handle musical chords.

Installation
------------

.. code:: sh

    $ pip install pychord

Usage
-----

Create a Chord
~~~~~~~~~~~~~~

.. code:: python

    >>> from pychord import Chord
    >>> c = Chord("Am7")
    >>> c.info()

    """
    Am7
    root=A
    quality=m7
    appended=[]
    on=None
    """

Transpose a Chord
~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from pychord import Chord
    >>> c = Chord("Am7/G")
    >>> c.transpose(3)
    >>> c

    "Cm7/Bb"

Get component notes
~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> from pychord import Chord
    >>> c = Chord("Am7")
    >>> c.components()

    ['A', 'C', 'E', 'G']

Supported Python Versions
-------------------------

-  2.7
-  3.3 and above

Links
-----

-  PyPI: https://pypi.python.org/pypi/pychord
-  GitHub: https://github.com/yuma-m/pychord

License
-------

-  MIT License

.. |Build Status| image:: https://travis-ci.org/yuma-m/pychord.svg?branch=master
   :target: https://travis-ci.org/yuma-m/pychord


