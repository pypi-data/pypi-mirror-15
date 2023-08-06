stringimporter
==================

let's you import raw string as real Python modules

How to use
==========

You can read the tests (in tests directory) or copy the following code.

.. code-block:: python

    import stringimporter

    module_from_thin_air = """
    def multiply_by_2():
        return lambda x: 2*x"""

    loader, mymodule = stringimporter.import_str('yihaaa', module_from_thin_air)

    hello_2 = mymodule.multiply_by_2()("hello ")
