Justbytes-GUI
=============

justbytes_gui is a simple library for demonstrating the display options
of the justbytes library.

There are a lot of display options, and it is a bit hard to remember all
their keywords.

Usage
-----

This library requires the justbytes library. It has one method, show(),
which is invoked on a justbytes.Range object. ::

    >>> from justbytes import *
    >>> number = Range(32, GiB)
    >>> from justbytes_gui import show
    >>> show(number)

The show() method opens a GUI displaying the number according to the default
options and allowing the user to experiment by changing the options.

The options are in two categories, those that may alter the value of the
number or of the unit displayed, and those that only alter the appearance.

Value Options
-------------

- Base -- the base in which the number is displayed. Ten is the most usual
  base, but the display options allow for any choice of base. Base 1000 is
  particularly useful when showing the value in SI units, base 1024 when
  showing the value in IEC units, since these choices of base also show
  the breakdown in sub-units.

- Units, IEC or SI -- IEC units are base 1024, SI are base 1000.

- Exact Value -- if this option is chosen, the highest units such that
  the resulting value is a whole number are chosen.

- Precision -- the maximum number of digits to the right of the radix.

- Limit -- a fraction, which multiplied by the appropriate factor for IEC or
  SI units, gives an upper limit on the size of the value to appear on the
  left of the radix. A choice of 1.0 with IEC units indicates that the value
  on the left of the radix must be strictly less than 1024 * 1.0.

- Rounding Method -- there are a number of rounding methods, with
  self-explanatory names.

- Unit -- if a particular unit, e.g., MB, is specified, this overrides other
  configuration operations.

Display Options
---------------

Display options are further grouped according to various categories.

Base Options
^^^^^^^^^^^^
These options determine how the base of the number is indicated.

- Prefix -- use one of the customary prefixes for either base 8 (0), or base
  16 (0x).

- Subscript -- use a subscript-like notation to indicate the base.

Digits Options
^^^^^^^^^^^^^^
These options determine how the digits are displayed.

- Use Letters -- use letters for digits with value larger than 9 in the
  customary way, i.e., a for 10, b for 11, and so forth.

- Use Capitals -- this is only meaningful if already using letters, and
  causes upper-case instead of lower-case letters to be used.

- Separator -- separator to separated digits from each other when other
  choices result in digits that require more than one character to represent.

Strip Options
^^^^^^^^^^^^^
These options control how trailing zeros are stripped.

- Strip All -- strip all trailing zeros.

- Strip Exact -- strip trailing zeros if the number displayed is exactly
  the same as the value it represents.

- Strip Whole -- like Strip Exact, but add the further restriction that only
  zeros appear on the right side.

Miscellaneous Options
^^^^^^^^^^^^^^^^^^^^^
These options fall into no obvious grouping.

- Show Relation -- indicate the relation of the value displayed to the value it   represents.
