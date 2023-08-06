========
Overview
========



CloudWatch-based monitoring for your servers.

* Free software: BSD license

Installation
============

::

    pip install cwmon

Documentation
=============

https://cwmon.readthedocs.io/

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

0.1.6 (2016-05-23)
-----------------------------------------

* First release on PyPI.


