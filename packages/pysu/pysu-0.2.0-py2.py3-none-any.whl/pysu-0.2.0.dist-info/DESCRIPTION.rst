========
Overview
========



Simple Python-based setuid+setgid+setgroups+exec. A port of https://github.com/tianon/gosu

* Free software: BSD license

Installation
============

::

    pip install pysu

Documentation
=============

Usage: pysu [-h] user[:group] command

Change user and exec command.

positional arguments:
  user
  command

optional arguments:
  -h, --help  show this help message and exit

Development
===========

To run the all tests run::

    tox


Changelog
=========

0.2.0 (2016-05-06)
------------------

* Allow using ":group" as argument, just like ``gosu`` (it will use the current user, but with the given group).

0.1.0 (2016-04-19)
------------------

* First release on PyPI.


