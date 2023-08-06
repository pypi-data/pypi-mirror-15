======
pyorcy
======

.. image:: https://travis-ci.org/markolopa/pyorcy.svg?branch=master
    :target: https://travis-ci.org/marklopa/pyorcy


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

Mechanism
---------

The user writes a python file which is the module. The function which
is to have a speedup is decorated with the @cythonize decorator.
Something like this:

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

A cython (``.pyx``) file is extracted from the python file.  This
extracted ``.pyx`` file will differ from the corresponding ``.py``
file is two ways:

- The comments starting with '#c ' are uncommented.
- The lines ending with '#p' are commented out.

You can check a complete example here:
`examples/compute_main.py<https://github.com/markolopa/pyorcy/blob/master/examples/compute_main.py>`_
and
`examples/compute_function.py<https://github.com/markolopa/pyorcy/blob/master/examples/compute_function.py>`_.

Getting started
---------------

Programmatic approach
.....................

With the `f()` function above, use:

.. code-block:: python

  import pyorcy
  from compute_function import f

  def execf(n, use_cython):
    pyorcy.USE_CYTHON = use_cython
    pyorcy.VERBOSE = True
    v = f(n, n)
    return v

So, basically import the `pyorcy` package and then set the
`USE_CYTHON` and `VERBOSE` module variables to your taste.  Easy uh?

There is a script in the examples/ folder that uses this technique.
Go to the main pyorcy directory and type::

  $ PYTHONPATH=. python examples/compute_main.py 1000
  Creating .../pyorcy/examples/compute_function_cy.pyx
  n = 1000 f = 5250000.0 use_cython = False time: 0.373s
  n = 1000 f = 5250000.0 use_cython = True time: 0.001s
  speedup: 311.9

Type the command once again to see what happens when the cython code is
already compiled and execution is immediate::

  $ PYTHONPATH=. python examples/compute_main.py 1000
  File .../pyorcy/examples/compute_function_cy.pyx already exists
  n = 1000 f = 5250000.0 use_cython = False time: 0.375s
  n = 1000 f = 5250000.0 use_cython = True time: 0.001s
  speedup: 314.2

Have a look at the examples/ directory for more hints on using pyorcy.

Via the pycorcy utility
.......................

There is another way to use the pyorcy package via its `pyorcy`
utility::

  $ time pyorcy -v --python examples/module_main.py 1000
  Running via Python mode
  n = 1000 f = 5250000.0 time: 0.528s

  real    0m0.748s
  user    0m0.720s
  sys     0m0.024s

Now, using Cython::

  $ time pyorcy -v --cython examples/module_main.py 1000
  Running via Cython mode
  Creating examples/compute_function_cy.pyx
  n = 1000 f = 5250000.0 time: 0.001s

  real    0m3.864s
  user    0m3.752s
  sys     0m0.088s

Although we see that the time for the computation is very small, the
global execution time for the script is quite large.  This is due to
the compilation time (.pyx -> .c creation + C compiling time).
However, the Cython version and the compiled extension are cached so
that next time that the module is executed the cached versions are
used instead::

  $ time pyorcy -v --cython examples/module_main.py 1000
  Running via Cython mode
  File examples/compute_function_cy.pyx already exists
  n = 1000 f = 5250000.0 time: 0.001s

  real    0m0.264s
  user    0m0.240s
  sys     0m0.020s

This utility allows to execute complete modules with the @cythonize
decorators in either '--python' (useful for debugging) or '--cython'
mode (the default).

Testing
-------

Before installing, you can test the package like this::

  $ py.test pyorcy

And after installing with (although this might fail if you install as
root and run tests as a regular user)::

  $ python -c"import pyorcy; pyorcy.test()

Installation
------------

If you have downloaded the sources, just install as usual::

  $ python setup.py install

or just install from PyPI directly::

  $ pip install pyorcy

and you are ready to go.

Troubleshooting
---------------

If you get::

 ImportError: Building module compute_cy failed: ['DistutilsPlatformError: Unable to find vcvarsall.bat\n']

like I did, contact me. I have found a workaround.

My use case
-----------

Here is why is pyorcy is important for my work.

I work in a team of engineers and mathematicians. They have learnt
python but not cython. Recently I have proposed a library with some
cython code. This added dependency has created resistance to the
acceptance of my code. Firstly, we met problems with compatibility
with Cython, Anaconda and virtual environments. Secondly, when my
collegues find bugs, they are not happy to depend on my help. They
want to do the debugging themselves. As they don't know Cython and are
uncomfortable with the compilation issues, I decided to provide two
versions of my code, one in pure python and another in Cython. Of
course maintaining two versions of my functions is not an advisable
approach. Using cython pure python mode is not an option since the
code needs advanced cython capabilities.

With pyorcy the user can then add a ``pyorcy.USE_CYTHON = False``
before the function call that they want to debug and proceed the
debugging in the pure python version, being able to add prints and
pbd without having to recompile, nor having to learn cython.

Before presenting pyorcy, a colleague suggested me to switch from
cython to numba. This would solve some of the issues, but I would
loose the freedom that cython gives (e.g. mix pure C code when needed)
and the wonderful html output (which gives us a perfect control of
what runs behind the scenes). Pyorcy comes partly as an answer to his
suggestion.
