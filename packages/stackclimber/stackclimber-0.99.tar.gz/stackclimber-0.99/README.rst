================
``stackclimber``
================

.. image:: https://travis-ci.org/drcloud/stackclimber.svg?branch=master
    :target: https://travis-ci.org/drcloud/stackclimber
.. image:: https://img.shields.io/pypi/v/stackclimber.svg
    :target: https://pypi.python.org/pypi/stackclimber
.. image:: https://img.shields.io/pypi/dd/stackclimber.svg
    :target: https://pypi.python.org/pypi/stackclimber

``stackclimber`` allows your function to find the module or script name of its
caller, or of its caller's caller.

.. code:: python

    from stackclimber import stackclimber


    assert stackclimber() == __name__
    assert stackclimber() == stackclimber(0)

With no arguments, it finds the current function's module name. With 1, it
finds that of its caller; with 2, that of its caller's caller, and so forth.

This functionality can be used to implement "automatic" imports that use some
information about the module into which they are being imported by overriding
a module's ``__getattr__``.
