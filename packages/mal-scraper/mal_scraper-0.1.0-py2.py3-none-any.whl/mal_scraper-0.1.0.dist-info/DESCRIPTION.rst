========
Overview
========



 MyAnimeList web scraper is a Python library for gathering data for analysis.


Usage
=====

Use the [online documentation](https://mal-scraper.readthedocs.io/), and just::

    pip install mal-scraper


Development
===========

After cloning, and creating a virtualenv, install the development dependencies::

    pip install -e .[develop]

You should install Python interpreters 3.3, 3.4, 3.5, and pypy because tox will
test on all of them.
(Hints: `Linux <https://askubuntu.com/questions/125342/how-can-i-install-python-2-6-on-12-04>`_.)

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

0.1.0 (2016-05-15)
-----------------------------------------

* First release on PyPI.


