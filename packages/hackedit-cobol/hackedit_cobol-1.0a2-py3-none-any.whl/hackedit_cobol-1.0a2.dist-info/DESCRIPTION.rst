.. image:: https://raw.githubusercontent.com/HackEdit/hackedit/master/docs/_static/banner.png

|

.. image:: https://img.shields.io/pypi/v/hackedit-cobol.svg
   :target: https://pypi.python.org/pypi/hackedit-cobol/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/hackedit-cobol.svg
   :target: https://pypi.python.org/pypi/hackedit-cobol/
   :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/hackedit-cobol.svg

.. image:: https://www.quantifiedcode.com/api/v1/project/07ea376eebe54a1180249e09461815ff/badge.svg
  :target: https://www.quantifiedcode.com/app/project/07ea376eebe54a1180249e09461815ff
  :alt: Code review

|

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/HackEdit/hackedit
   :target: https://gitter.im/HackEdit/hackedit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

About
=====

A set of plugins that add COBOL support to `HackEdit`_.

Features:
---------

- `pyqode.cobol`_ editor integration (syntax highlighter, code completion, goto, code folding,...)
- support for OpenCOBOL 1.1 and GnuCOBOL 2.0 compiler (MSVC based compiler are also supported on Windows)
- support for custom parsers + premade setups for DBPRE and EsqlOC
- two builtin workspaces:

  - project mode: specify which files are part of the project and compile them all at once.
  - single file mode: compile the current editor (very similar to OpenCobolIDE)

- support for multiple compiler configuration (you can choose which config is the main one and you can select secondary configuration to be run when you build your project/file).
- tool for computing field offset


In the future, we plan to add the following features:

- GnuCOBOL 2 debugger integration
- Support for standard build tools (makefile, autotools)


Requirements
------------

- `hackedit`_

.. _HackEdit: http://github.com/HackEdit/hackedit
.. _pyqode.cobol: http://github.com/pyQode/pyqode.cobol


Installation
------------

::

   pip3 install hackedit-cobol --pre --upgrade

The plugin does not provide the GnuCOBOL compiler, you need to install it by yourself:

- on **Windows**, the plugin will try to use the compiler bundled with `OpenCobolIDE`_.
- on **OSX**, you can easily install the compiler by running ``brew install gnu-cobol`` or ``brew install gnu-cobol --devel`` for GnuCOBOL 2.0
- on **GNU/Linux**, you should use your package manager or install from source if it is not available (you will likely find the ``open-cobol`` or ``gnu-cobol`` package)

.. _OpenCobolIDE: https://github.com/OpenCobolIDE/OpenCobolIDE


