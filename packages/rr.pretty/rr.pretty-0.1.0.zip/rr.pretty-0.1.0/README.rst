=========
rr.pretty
=========

This module exposes a few functions and a class decorator to make the task of writing ``__repr__()`` and ``__str__()`` for custom classes much easier. It will display a list of nicely formatted ``(attr, val)`` pairs with custmizable separator and formatting for each pair.

Let's look at an example:

.. code-block:: python

    from rr import pretty

    class foo(object):
        __str__ = pretty.str
        __repr__ = pretty.repr
        __info__ = pretty.info(["x", "y", "z"])

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    f = foo(1, 2, 3)
    print repr(f)  # see for yourself :)
    print str(f)

Now, let's do the same, only this time we'll use the ``klass()`` class decorator:

.. code-block:: python

    from rr import pretty

    @pretty.klass
    class foo(object):
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    f = foo(1, 2, 3)
    print repr(f)  # see for yourself :)
    print str(f)

We even left out the attribute list, and ``pretty.info()`` (which is what ``pretty.klass()`` uses behind the scenes) builds it for us. That's it! You get nice ``__repr__()`` and ``__str__()`` methods for free.


Installation
============

From PyPI ("stable" release):

.. code-block:: bash

    pip install rr.pretty

From the Git repo:

.. code-block:: bash

    git clone https://github.com/2xR/rr.pretty.git
    pip install ./rr.pretty


Contributing
============

Contributions are welcome through github pull requests (tests would be nice to have... :P)

And if you're using the library and would like to say *"thanks!"* and/or keep me working on it, why not `buy me a beer <https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=2UMJC8HSU8RFJ&lc=PT&item_name=DoubleR&item_number=github%2f2xR%2fpaypal&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted>`_?
