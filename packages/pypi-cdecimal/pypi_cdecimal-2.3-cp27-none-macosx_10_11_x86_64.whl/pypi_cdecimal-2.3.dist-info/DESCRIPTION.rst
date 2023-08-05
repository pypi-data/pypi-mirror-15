Overview
--------

The ``cdecimal`` package is a fast drop-in replacement for the ``decimal`` module
in Python's standard library. Both modules provide complete implementations of
Mike Cowlishaw/IBM's ``General Decimal Arithmetic Specification``.

Testing
-------

Both ``cdecimal`` and the underlying library - ``libmpdec`` - are extremely
well tested. ``libmpdec`` is one of the few open source projects with 100%
code coverage. ``cdecimal`` is rigorously tested against ``decimal.py``.

Short benchmarks
----------------

Typical performance gains are between 30x for I/O heavy benchmarks
and 80x for numerical programs. In a database benchmark, cdecimal
exhibits a speedup of 12x over decimal.py.

+---------+-------------+--------------+-------------+
|         |   decimal   |   cdecimal   |   speedup   |
+=========+=============+==============+=============+
|   pi    |    42.75s   |    0.58s     |     74x     |
+---------+-------------+--------------+-------------+
| telco   |   172.19s   |    5.68s     |     30x     |
+---------+-------------+--------------+-------------+
| psycopg |     3.57s   |    0.29s     |     12x     |
+---------+-------------+--------------+-------------+

Documentation
-------------

Since ``cdecimal`` is compatible with ``decimal.py``, the official documentation
is valid. For the few remaining differences, refer to the second link.

* `Decimal module <http://docs.python.org/dev/py3k/library/decimal.html>`_
* `Differences between cdecimal and decimal <http://www.bytereef.org/mpdecimal/doc/cdecimal/index.html>`_

Linux Notes
-----------

The build process requires a working C compiler and a *full* Python install with
development headers. Linux distributions often ship the Python header files as
a separate package, called *python-dev* or *python-devel*.

Install headers on Debian/Ubuntu:

* ``sudo apt-get install python-dev``

Windows Notes
-------------

* `Binary installers <http://www.bytereef.org/mpdecimal/download.html>`_

Links
-----

* `cdecimal project homepage <http://www.bytereef.org/mpdecimal/index.html>`_
* `cdecimal benchmarks <http://www.bytereef.org/mpdecimal/benchmarks.html>`_



