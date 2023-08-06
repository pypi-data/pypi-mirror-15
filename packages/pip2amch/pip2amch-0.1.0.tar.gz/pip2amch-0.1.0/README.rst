===============================
pip2amch
===============================

| |docs| |travis| |appveyor| |coveralls| |landscape| |scrutinizer|
| |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/pip2amch/badge/?style=flat
    :target: https://readthedocs.org/projects/pip2amch
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/svetlyak40wt/pip2amch/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/svetlyak40wt/pip2amch

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/svetlyak40wt/pip2amch?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/svetlyak40wt/pip2amch

.. |coveralls| image:: http://img.shields.io/coveralls/svetlyak40wt/pip2amch/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/svetlyak40wt/pip2amch

.. |landscape| image:: https://landscape.io/github/svetlyak40wt/pip2amch/master/landscape.svg?style=flat
    :target: https://landscape.io/github/svetlyak40wt/pip2amch/master
    :alt: Code Quality Status

.. |version| image:: http://img.shields.io/pypi/v/pip2amch.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pip2amch

.. |downloads| image:: http://img.shields.io/pypi/dm/pip2amch.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/pip2amch

.. |wheel| image:: https://pypip.in/wheel/pip2amch/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pip2amch

.. |supported-versions| image:: https://pypip.in/py_versions/pip2amch/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pip2amch

.. |supported-implementations| image:: https://pypip.in/implementation/pip2amch/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/pip2amch

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/svetlyak40wt/pip2amch/master.png?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/svetlyak40wt/pip2amch/

Command to transform pip's requirements.txt into a csv for batch upload to https://allmychanges.com.
It allows to sync your requirements with AllMyChanges and to supbscribe on their updates.

* Free software: BSD license

Installation
============

::

    pip install pip2amch


Usage
=====

To use pip2amch in a project::

  pip2amch --tag my-project requirements.txt | amch push

This will push all requirements from the file to the service
https://allmychanges.com, where you can subscribe on their
release notes.


Documentation
=============

https://pip2amch.readthedocs.org/

Development
===========

To run the all tests run::

    tox

.. include:: CHANGELOG.rst
