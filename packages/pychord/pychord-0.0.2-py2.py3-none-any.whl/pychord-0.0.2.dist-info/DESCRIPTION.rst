pychord
=======

A library to handle musical chords in python. If you want to know more
about chord, please see https://en.wikipedia.org/wiki/Chord\_(music)

Installation
------------

.. code:: sh

    $ pip install pychord

Usage
-----

.. code:: python

    >>> from pychord import Chord
    >>> c = Chord("Am7")
    >>> print c.info()
    Am7
    root=A
    quality=m7
    appended=[]
    on=None


