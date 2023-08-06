==============
python-lz4-raw
==============

.. image:: https://secure.travis-ci.org/haohui/python-lz4-raw.png?branch=master

Inspired by the `python-lz4 <https://pypi.python.org/pypi/lz4>`_ library, this package provides yet another bindings for the `lz4 compression library <http://www.lz4.org>`_ by Yann Collet. Compared to the python-lz4 library, it provides bindings to the unframed API including `LZ4_compress_default()` and `LZ4_decompress_safe()` so that it can be used along with the `python-hadoop <https://github.com/matteobertozzi/Hadoop/tree/master/python-hadoop>`_ package to read data for customized framing such as the Hadoop SequenceFile format.

Install
=======

The package is hosted on `PyPI <http://pypi.python.org/pypi/lz4>`_::

    $ pip install lz4-raw
    $ easy_install lz4-raw
