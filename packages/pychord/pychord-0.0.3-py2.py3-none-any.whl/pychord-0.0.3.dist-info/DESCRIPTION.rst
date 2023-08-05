pychord
=======

A library to handle musical chords in python.

Installation
------------

.. code:: sh

    $ pip install pychord

Usage
-----

Create a Chord
~~~~~~~~~~~~~~

.. code:: python

    from pychord import Chord
    c = Chord("Am7")
    print c.info()

::

    Am7
    root=A
    quality=m7
    appended=[]
    on=None

Transpose a Chord
~~~~~~~~~~~~~~~~~

.. code:: python

    from pychord import Chord
    c = Chord("Am7/G")
    c.transpose(3)
    print c

::

    Cm7/Bb

Links
-----

-  https://pypi.python.org/pypi/pychord
-  https://github.com/yuma-m/pychord

License
-------

MIT License


