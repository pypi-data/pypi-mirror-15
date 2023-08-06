Debug Context Manager
=====================

Super simple context manager to wrap a block of code with a debug
message.

Usage
=====

.. code:: python

    from debug_context_manager import debug

    with debug("Doing this stuff"):
        # some code

    with debug("Doing other stuff", "and finished!"):
        # other code



