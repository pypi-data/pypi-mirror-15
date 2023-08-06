========
Overview
========



A magic shortcut to generate __repr__ methods for your classes.

* Free software: BSD license

Installation
============

::

    pip install repr

This package contains a single module ``magic_repr`` called so
to not conflict with standart python's ``repr``.

Reasoning
=========

What do you think each time, writing such code?

.. code:: python

  def __repr__(self):
      return """
  Issue(changelog={self.changelog},
        type={self.type},
        comment={self.comment},
        created_at={self.created_at},
        resolved_at={self.resolved_at})""".format(self=self).strip().encode('utf-8')

Isn't this much better and readable?

.. code:: python

      __repr__ = make_repr('changelog', 'type', 'comment', 'created_at', 'resolved_at')


And this produces much nicer output:

.. code:: python

  <Issue changelog=<Changelog namespace=u'python'
                              name=u'geocoder'
                              source=u'https://github.com/DenisCarriere/geocoder'>
         type=u'wrong-version-content'
         comment=u'AllMyChanges should take release notes from the web site.'
         created_at=datetime.datetime(2016, 6, 17, 6, 44, 52, 16760, tzinfo=<UTC>)
         resolved_at=None>

Another advantage of the magic_repr
-----------------------------------

Is it's recursiveness. If you use ``magic_repr`` for your objects and they
include each other, then representation of the parent object will include
child objects properly nested:

.. code:: python

  <Foo bars={1: <Bar first=1
                     second=2
                     third=3>,
             2: <Bar first=1
                     second=2
                     third=3>,
             u'три': <Bar first=1
                          second=2
                          third=3>}>

And all this for free! Just do ``__repr__ = make_repr()``.

Usage
=====

For simple cases it is enough to call ``make_repr`` without arguments. It will figure out
which attributes object has and will output them sorted alphabetically.

You can also specify which attributes you want to include in "representaion":

.. code:: python

  __repr__ = make_repr('foo', 'bar')

And to specify a function to create a value for an attribute, using keywords:

.. code:: python

  class Some(object):
      def is_active(self):
          return True

  Some.__repr__ = make_repr(active=Some.is_active)

Pay attention, that in this case ``__repr__`` was created after the class definition.
This is because inside of the class it can't reference itself.

Documentation
=============

https://python-repr.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

Changelog
=========

0.3.0 (2016-06-20)
------------------

* Now ``make_repr`` can be used for recursive datastructures.

0.2.1 (2016-06-19)
------------------

* Documentation improved.

0.2.0 (2016-06-19)
------------------

* Better handling of nested datastructure.
* Callables as source of the attribute's value.
* Some documentation.

0.1.0 (2016-06-09)
------------------

* First release on PyPI.


