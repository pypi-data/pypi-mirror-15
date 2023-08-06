======================
Announcing pyorcy 0.1
======================

What's new
==========

This is the first release of pyorcy.  Your input is more than welcome!

For a more detailed change log, see:

https://github.com/markolopa/pyorcy/blob/master/RELEASE_NOTES.rst


What it is
==========

Pyorcy has 2 purposes:

#. Allow the mix of python and cython code in a single file. This can
   also be done with cython's "pure python" mode, but with import
   limitations. pyorcy gives you the full cython super-powers.

#. Launch an automatic compilation, triggered by a function
   decorator. This mechanism is similar to what numba offers.

So basically, you can develop and debug using the python mode.  When
you are happy with your function, then you just annotate the variables
and add the decorator for automatic Cython code generation and
compilation.  Simple.

Here it is a simple example of how pyorcy code looks like:

.. code-block:: python

  import pyorcy
  import numpy as np
  #c cimport cython

  def value(i, j, price, amount): #p
  #c @cython.boundscheck(False)
  #c cdef double value(int i, int j, double[:] price, double[:] amount):
      #c cdef int a, p
      #c cdef double v
      v = price[i] * amount[j]
      return v

  @pyorcy.cythonize #p
  def f(n, m): #p
  #c def f(int n, int m):
      #c cdef int i, j
      #c cdef double v
      #c cdef double[:] price
      #c cdef double[:] amount
      price = np.linspace(1, 2, n)
      amount = np.linspace(3, 4, m)
      v = 0
      for i in range(n):
          for j in range(m):
              v += value(i, j, price, amount)
      return v

You can check a complete example here:
`examples/compute_main.py<https://github.com/markolopa/pyorcy/blob/master/examples/compute_main.py>`_
and
`examples/compute_function.py<https://github.com/markolopa/pyorcy/blob/master/examples/compute_function.py>`_.


More info
=========

Visit the main pyorcy site repository at:
http://github.com/markolopa/pyorcy

License is MIT:
https://github.com/markolopa/pyorcy/blob/master/LICENSE.txt


----

Enjoy!
