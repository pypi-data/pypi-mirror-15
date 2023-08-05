brotlipy
========

This library contains Python bindings for the reference Brotli encoder/decoder,
`available here`_. This allows Python software to use the Brotli compression
algorithm directly from Python code.

To use it simply, try this:

.. code-block:: python

    import brotli
    data = brotli.decompress(compressed_data)

More information can be found `in the documentation`_.

.. _available here: https://github.com/google/brotli
.. _in the documentation: https://brotlipy.readthedocs.org

License
-------

The source code of brotlipy is available under the MIT license. Brotli itself
is made available under the Version 2.0 of the Apache Software License. See the
LICENSE and libbrotli/LICENSE files for more information.

Authors
-------

brotlipy is maintained by Cory Benfield.


Changelog
=========

0.3.0 (2016-05-11)
------------------

Update to v0.3.0 of the Brotli library.

0.2.0 (2015-10-05)
------------------

Fix broken ``brotli.compress`` support on Windows.

0.1.3 (2015-10-05)
------------------

- Added basic for ``brotli.compress`` through a C wrapper included in this
  library.


