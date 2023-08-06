Contextualized tracebacks
=========================

If you have ever wrote a Python program that processes large input files you probably have been in a situation where you get an error on certain file and line. You may get a traceback telling you have e.g. a ``KeyError`` but still don't know what line in that text file provoked it.

Then you may start adding ``print(line)`` calls every time a line is processed, but that's quirky, clutters your terminal quickly and you'll have to eventually remove it, only to later add it when the next bug hits.

This module is an alternative to improve this kind of debugging issue, making it clean and robust, whilst providing a easy to use API.

This module works by providing you with a context object where you can set state variables like file name and line number. When an unhandled exception is raised, this module catches it and prints the value of the state variables along with the traceback.

Example code:

.. code-block:: python

    from contextualized import contextualized_tracebacks

    def main():
        dcontext.file = 'hello.txt'
        a()

    def a():
        dcontext.line = 20
        b()

    def b():
        # buggy code
        nonexistent += 1

    with contextualized_tracebacks(['file', 'line', 'character']) as dcontext:
        main()

This program will show this once run:

.. code-block::

    Traceback (most recent call last):
      File "contextualized_example.py", line 16, in <module>
        main()
      File "contextualized_example.py", line 5, in main
        a()
      File "contextualized_example.py", line 9, in a
        b()
      File "contextualized_example.py", line 13, in b
        nonexistent += 1
    UnboundLocalError: local variable 'nonexistent' referenced before assignment
    The exception was caught on file 'hello.txt', line 20.

The context information is right after the traceback. Notice how only non ``None`` fields are shown. They also preserve the order from the ``contextualized_tracebacks()`` call.

Overriding the traceback print function
---------------------------------------

You can override the default traceback print with the ``print_tb`` argument. For example, this example will print the context **before** the traceback.

.. code-block:: python

    from contextualized import contextualized_tracebacks

    def main():
        dcontext.file = 'hello.txt'
        a()

    def a():
        dcontext.line = 20
        b()

    def b():
        # buggy code
        nonexistent += 1

    def my_print_tb(context, tb_info):
        import traceback
        import sys

        print('An exception was caught on %s.' % context._to_prose(),
              file=sys.stderr)
        traceback.print_exception(*tb_info)

    with contextualized_tracebacks(['file', 'line', 'character'],
                                   print_tb=my_print_tb) as dcontext:
        main()

This will be the new output:

.. code-block::

    An exception was caught on file 'hello.txt', line 20.
    Traceback (most recent call last):
      File "contextualized_example.py", line 25, in <module>
        main()
      File "contextualized_example.py", line 5, in main
        a()
      File "contextualized_example.py", line 9, in a
        b()
      File "contextualized_example.py", line 13, in b
        nonexistent += 1
    UnboundLocalError: local variable 'nonexistent' referenced before assignment

Links
-----

* `Project home page <https://github.com/ntrrgc/contextualized>`_ (GitHub)
* `Contextualized in PyPI <https://pypi.python.org/pypi/contextualized>`_

Changelog
---------

* **1.0**: Initial release.
* **1.1**: SystemExit exceptions no longer are catched, thus triggering normal ``exit()`` by the interpreter.
* **1.2**: Modified ``setup.py`` to install successfully with ``LANG=C``.
* **1.3**: Fixed a bug that caused contextualized not to work in Python 2.

License
-------

This module is under the MIT License.

Copyright (c) 2015 Juan Luis Boya García


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
