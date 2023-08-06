dbgcode: Write debug code with confidence

dbgcode is a python package that make it easy
to remove debug code after you finish debugging


Installation
------------

.. code-block:: bash

    $ pip install dbgcode

Quick Start
-----------

example usage:
file: f.py

.. code-block:: python

    x = []
    for i in range(1, 100):
        for j in range(1, 100):
            # dbg
            print("i", i)
            print("j", j)
            # /dbg
            if i % 3 == 0 and j % 3 == 0:
                print("(i, j) ", (i, j))  # _dbg
                x.append((i, j))


save this file and then in the command line

.. code-block:: bash

    $ dbgcode clean f.py

the result is:
.. code-block:: python

    x = []
    for i in range(1, 100):
        for j in range(1, 100):
            if i % 3 == 0 and j % 3 == 0:
                x.append((i, j))

LICENSE
-------
**MIT**
