Little CMS Python Bindings
==========================

`SWIG <http://swig.org>`_ generated Python bindings for v2.7 of `Little CMS <http://www.littlecms.com>`_.

This distribution contains the necessary C source files from littlecms in the c_sources directory.


Installing
==========

The distributed product is best installed by users using pip:
    pip install littlecms

Building in Development Mode
============================

Building the product during further development is best done in the setuptools
development mode. From the base of the repo, use this command:
    setup develop --install-dir=<dir>

where <dir> is a location on your PYTHONPATH. This requires that you have both
setuptools and the appropriate C build tools available for the target version of
Python [On Windows, that's Visual Studio 2015 for Python 3.5 and Visual Studio 2010
for Python 3.3-3.4].

Installing setuptools
=====================

Follow the instructions at https://pypi.python.org/pypi/setuptools. The
recommended method is to download ez_setup.py and run it using the target Python
environment.
NB. This step isn't required for Python 3.4+ because setuptools are pre-installed
    in the Python distribution.

Generating the SWIG Wrapper
===========================

This package contains swig/littlecms_wrap.cpp and littlecms/littlecms.py, which
form a pre-generated Python3 SWIG wrapper for the littlecms library.
If you need to regenerate the wrapper, the SWIG source files are also included.
This is the command line used on Windows:

    swig -python -py3 -Ic_sources/include -I"C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\include" -outdir littlecms -o swig/littlecms_wrap.cpp  swig/littlecms.i

This command requires that SWIG is installed, and that the VS2015 header files are
available in the given location.
NB. This command is for Python 3.5+ which requires VS2015 (includes Visual C v14).
    Python 3.3-3.4 requires VS2010, so change this command to use headers from
    "Microsoft Visual Studio 10.0" instead.
    Actually, for the purpose of this command only, it doesn't make any difference
    which headers are used for either version of Python.
