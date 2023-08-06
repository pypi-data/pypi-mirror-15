=========
rr.approx
=========

Approximate floating point arithmetic library. This simple module can be used to compare numbers using a relative and absolute tolerance, to mitigate floating point rounding errors.

.. code-block:: python

    from rr.approx import Approx

    x = Approx(0.1) * 3
    print x == 0.3  # True

The ``Approx`` class is very simple to use as a replacement for "regular" floats -- you can use ``Approx`` objects instead of floats in most (if not all) contexts: arithmetic and comparisons.

The ``ApproxContext`` class, also accessible as ``Approx.Context``, provides a context manager to temporarily modify the module's tolerance parameters.

.. code-block:: python

    from rr.approx import Approx

    print Approx.Context()  # display current context
    Approx.Context(1e-4, 1e-2).apply()  # permanently modify tolerances
    print Approx.Context()
    with Approx.Context(rtol=1e-5, atol=1e-3):  # temporary modification
        print Approx.Context()
    print Approx.Context()


Installation
------------

.. code-block:: bash

    pip install rr.approx


