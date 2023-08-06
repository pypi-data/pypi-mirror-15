#!/usr/bin/env python
# filename: decorators.py


#
# Copyright (c) 2015 Bryan Briney
# License: The MIT license (http://opensource.org/licenses/MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


def lazy_property(func):
    '''
    Wraps a property to provide lazy evaluation. Eliminates boilerplate.
    Also provides for setting and deleting the property.

    Use as you would use the @property decorator::

        # OLD:
        class MyClass():
            def __init__()
                self._compute = None

            @property
            def compute(self):
                if self._compute is None:
                    # computationally intense stuff
                    # ...
                    # ...
                    self._compute = result
                return self._compute

            @compute.setter
            def compute(self, value):
                self._compute = value


        # NEW:
        class MyClass():

            def __init__()

            @property
            def compute(self):
                # computationally intense stuff
                # ...
                # ...
                return result

    .. note:

        Properties wrapped with ``lazy_property`` are only evaluated once.
        If the instance state changes, lazy properties will not be
        re-evaulated and must be updated manually::

            c = MyClass(data)
            prop = c.lazy_property

            # If you update some data that affects c.lazy_property
            c.data = new_data

            # You need to recompute c.lazy_property manually
            c.lazy_property = new_lazy_property
    '''
    attr_name = '_lazy_' + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    @_lazy_property.deleter
    def _lazy_property(self):
        if hasattr(self, attr_name):
            delattr(self, attr_name)

    @_lazy_property.setter
    def _lazy_property(self, value):
        setattr(self, attr_name, value)

    return _lazy_property


def coroutine(func):
    '''
    Initializes a coroutine -- essentially it just takes a
    generator function and calls generator.next() to get
    things going.
    '''
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start
