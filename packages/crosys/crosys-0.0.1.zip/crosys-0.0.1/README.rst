.. image:: https://img.shields.io/pypi/v/crosys.svg

.. image:: https://img.shields.io/pypi/l/crosys.svg

.. image:: https://img.shields.io/pypi/pyversions/crosys.svg


Welcome to crosys Documentation
========================================
Like `six <https://pypi.python.org/pypi/six>`_ is for python2/3 compatibility, crosys (cross system) is for Windows/MacOS/Linux Compatibility.


**Quick Links**
-------------------------------------------------------------------------------
- `GitHub Homepage <https://github.com/MacHu-GWU/crosys-project>`_
- `PyPI download <https://pypi.python.org/pypi/crosys>`_
- `Install <install_>`_


.. _install:

Install
-------------------------------------------------------------------------------

``crosys`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install crosys

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade crosys


Usage
-------------------------------------------------------------------------------
.. code-block:: python

	>>> import crosys
	>>> corsys.WINDOWS
	True
	>>> crosys.MACOS
	False
	>>> crosys.LINUX
	False
	>>> crosys.SP_PATH # site-packages path
	C:\Python34\lib\site-packages
	>>> crosys.PROGRAM_FILES_64
	C:\Program Files
	>>> crosys.PROGRAM_FILES_32
	C:\Program Files (x86)