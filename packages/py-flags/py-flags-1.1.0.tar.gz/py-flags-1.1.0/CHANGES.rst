
CHANGES
=======


v1.1.0
------

*Release date: 2016-04-29*

- Extended README.rst with full documentation. Before it contained only a "Quick Overview" section.
- Added ``Flags.__dotted_single_flag_str__``.
- The ``Flags.data`` property returns ``UNDEFINED`` for special flags and flag combinations.
- Added the ``__pickle_int_flags__`` class attribute that can be set to ``True`` in order to force pickle to save
  the ``int`` representation of flags instead of the default ``to_simple_str()`` representation.
- Added the ``@unique_bits`` decorator that can be used to forbid overlapping bits between the values of flags.
- Added the ``@unique`` decorator that can be used to forbid aliases in a flags class. (An alias is a flag that
  has the exact same value as a previously declared flag.)
- Added ``__repr__`` for flags classes.


v1.0.1
------

*Release date: 2016-04-23*

- Fixed the README.rst in the distribution.


v1.0.0
------

*Release date: 2016-04-23*

Initial release on pypi.
