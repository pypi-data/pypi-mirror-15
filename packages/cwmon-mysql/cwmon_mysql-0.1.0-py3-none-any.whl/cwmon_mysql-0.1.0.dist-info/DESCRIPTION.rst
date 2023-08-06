========
Overview
========



A cwmon plugin for monitoring MySQL.

* Free software: BSD license

Installation
============

::

    pip install cwmon-mysql

Documentation
=============

https://cwmon-mysql.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2016-05-24)
-----------------------------------------

* First release on PyPI.


