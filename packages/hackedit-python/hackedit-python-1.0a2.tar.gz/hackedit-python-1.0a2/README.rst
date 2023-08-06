.. image:: https://raw.githubusercontent.com/HackEdit/hackedit/master/docs/_static/banner.png

|

.. image:: https://img.shields.io/pypi/v/hackedit-python.svg
   :target: https://pypi.python.org/pypi/hackedit-python/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/hackedit-python.svg
   :target: https://pypi.python.org/pypi/hackedit-python/
   :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/hackedit-python.svg

.. image:: https://www.quantifiedcode.com/api/v1/project/d91d10d61b90454382c91d6b9bcb73b2/badge.svg
  :target: https://www.quantifiedcode.com/app/project/d91d10d61b90454382c91d6b9bcb73b2
  :alt: Code review

|

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/HackEdit/hackedit
   :target: https://gitter.im/HackEdit/hackedit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


About
=====

A set of plugins that add Python support to `HackEdit`_.

Features:
---------

- ability to run scripts (or the selected text of an editor) and manage
  project run configuration
- `pyqode.python`_ integration:

  - syntax highlighting
  - code completion (based on the `jedi`_ code completion engine)
  - pep8 + pyflakes on the fly analysis
  - smart indentation
  - go to definition
  - call tips
  - documentation viewer
- refactoring (with `rope`_)
- package manager interface
- support for virtualenv and custom intepreters


Requirements
------------

The following packages are needed:

- `hackedit`_
- `docutils`_


The following packages are included in a "vendor" subpackage.

- `rope`_
- `virtualenv`_


Installation
------------

::

    pip3 install hackedit-python --pre --upgrade

.. _HackEdit: https://github.com/HackEdit/hackedit
.. _docutils: https://pypi.python.org/pypi/docutils
.. _rope: https://pypi.python.org/pypi/rope_py3k
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _pyqode.python: https://github.com/pyQode/pyqode.python
.. _jedi: https://pypi.python.org/pypi/jedi
