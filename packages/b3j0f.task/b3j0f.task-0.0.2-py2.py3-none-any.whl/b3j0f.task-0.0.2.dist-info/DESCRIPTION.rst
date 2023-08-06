Description
-----------

Python object configuration library in reflective and distributed concerns.

.. image:: https://img.shields.io/pypi/l/b3j0f.task.svg
   :target: https://pypi.python.org/pypi/b3j0f.task/
   :alt: License

.. image:: https://img.shields.io/pypi/status/b3j0f.task.svg
   :target: https://pypi.python.org/pypi/b3j0f.task/
   :alt: Development Status

.. image:: https://img.shields.io/pypi/v/b3j0f.task.svg
   :target: https://pypi.python.org/pypi/b3j0f.task/
   :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/b3j0f.task.svg
   :target: https://pypi.python.org/pypi/b3j0f.task/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/b3j0f.task.svg
   :target: https://pypi.python.org/pypi/b3j0f.task/
   :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/wheel/b3j0f.task.svg
   :target: https://travis-ci.org/b3j0f/task
   :alt: Download format

.. image:: https://travis-ci.org/b3j0f/task.svg?branch=master
   :target: https://travis-ci.org/b3j0f/task
   :alt: Build status

.. image:: https://coveralls.io/repos/b3j0f/task/badge.png
   :target: https://coveralls.io/r/b3j0f/task
   :alt: Code test coverage

.. image:: https://img.shields.io/pypi/dm/b3j0f.task.svg
   :target: https://pypi.python.org/pypi/b3j0f.task/
   :alt: Downloads

.. image:: https://readthedocs.org/projects/b3j0ftask/badge/?version=master
   :target: https://readthedocs.org/projects/b3j0ftask/?badge=master
   :alt: Documentation Status

.. image:: https://landscape.io/github/b3j0f/task/master/landscape.svg?style=flat
   :target: https://landscape.io/github/b3j0f/task/master
   :alt: Code Health

Links
-----

- `Homepage`_
- `PyPI`_
- `Documentation`_

Installation
------------

pip install b3j0f.task

Features
--------

This library performs execution of registered python routines.

Example
-------

.. code-block:: python

    from b3j0f.task import register, run

    @register
    @register('mytask')
    def task(param):
        return param

    register(task, name='lastname')

    assert run('task', {'param': 1}) == 1
    assert run('mytask', {'param': 1}) == 1
    assert run('lastname', {'param': 1}) == 1

Perspectives
------------

- wait feedbacks during 6 months before passing it to a stable version.
- Cython implementation.

Donation
--------

.. image:: https://cdn.rawgit.com/gratipay/gratipay-badge/2.3.0/dist/gratipay.png
   :target: https://gratipay.com/b3j0f/
   :alt: I'm grateful for gifts, but don't have a specific funding goal.

.. _Homepage: https://github.com/b3j0f/task
.. _Documentation: http://b3j0fconftask.readthedocs.org/en/master/
.. _PyPI: https://pypi.python.org/pypi/b3j0f.task/


