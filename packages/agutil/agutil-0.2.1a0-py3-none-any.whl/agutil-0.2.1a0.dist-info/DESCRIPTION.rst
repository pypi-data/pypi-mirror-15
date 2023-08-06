agutil
======

-  Master build status: |Master Build Status|
-  Development build status: |Dev Build Status|

A collection of python utilities

**Version:** 0.2.1a

Tools:


-  search\_range (A utility for manipulating numerical ranges)
-  status\_bar (A simple progress bar indicator)

The **bio** package: \* maf2bed (A command line utility for parsing a
.maf file, converting coordinates from 1-based (maf standard) to 0-based
(bed standard)) \* tsvmanip (A command line utility for filtering,
rearranging, and modifying tsv files)

SEARCH\_RANGE
-------------

The ``agutil`` module includes the class, ``search_range`` A
``search_range`` class instance keeps track of a set of numerical ranges
Any number of ranges can be included or excluded from the instance A
single point, or range of points can be checked against the instance for
intersection Multiple instances can be combined with union, difference,
and intersection operators to produce new ``search_ranges`` The set of
points in the search range is implemented as a bitset for efficiency

API


-  search\_range(start=0, stop=0, fill=True) *(constructor)* Creates a
   new ``search_range`` instance with the range [*start*, *stop*)
   included ``search_range.check(i)`` will return True for any point
   within [*start*, *stop*)

-  search\_range.add\_range(start, stop) Adds the range [*start*,
   *stop*) to the set of points in the search range

-  search\_range.remove\_range(start, stop) Removes the range
   [s\_tart\_, *stop*) from the set of points in the search range

-  search\_range.check(coord) Returns True if *coord* exists within the
   set of points included in the search range Returns False otherwise

-  search\_range.check\_range(start, stop) Returns True if any point
   within the range [*start*, *stop*) is included in the search range
   Returns False otherwise

-  search\_range.union(other)
-  search\_range.difference(other)
-  search\_range.intersection(other) Returns a new search\_range whose
   set of points is the result of the union, difference, or intersection
   (respectively) of this search\_range and *other* These methods can
   also be accessed through the following binary operators:

   -  Union: *a\|b* *a+b*
   -  Difference: *a-b*
   -  Intersection: *a&b* \_a\*b\_

-  search\_range.\_\_iter\_\_() *(iteration)* search\_ranges support
   iteration, which produces a sequence of points included in the range

-  search\_range.gen\_ranges() Returns a generator which yields pairs of
   [start, stop) coordinates for each continuous set of points in the
   range

-  search\_range.range\_count() Returns the number of points included in
   the range

-  search\_range.\_\_str\_\_() Produces a string which lists the ranges
   produced by gen\_ranges()

-  search\_range.\_\_repr\_\_() Produces a string which lists each point
   included in the range

-  search\_range.\_\_bool\_\_() Returns True if there is at least one
   point included in the range

STATUS\_BAR
-----------

The ``agutil`` module includes the class, ``status_bar`` A
``status_bar`` instance provides a status indicator which can be updated
at any time The display is only updated when necessary, so there is
minimal drawback for updating the instance frequently

API


-  status\_bar(maximum, show\_percent = False, init=True, prepend="",
   append="", cols=int(get\_terminal\_size()[0]/2),
   update\_threshold=.00005, debugging=False, transcript=None)
   *(constructor)* Creates a new status\_bar instance ranging from 0 to
   *maximum*

*show\_percent* toggles whether or not a percentage meter should be
displayed to the right of the bar

*init* sets whether or not the status\_bar should immediately display.
If set to false, the bar is displayed at the first update

*prepend* is text to be prepended to the left of the bar. It will always
remain to the left of the bar as the display updates. **WARNING**
Prepended text offsets the bar. If any part of the bar (including
prepended or appended text) extends beyond a single line on the console,
the status bar will not display properly. Prepended text should be kept
short

*append* is text to be appended to the right of the bar. It will always
remain to the right of the bar as the display updates. **WARNING**
Appended text extends the display. If any part of the bar (including
prepended or appended text) extends beyond a single line of the console,
the status bar will not display properly. Appended text should be kept
short

*cols* sets how long the bar should be. It defaults to half the terminal
size

*update\_threshold* sets the minimum change in percentage to trigger an
update to the percentage meter

*debugging* triggers the status\_bar to never print to stdout. If set
true, no output will be produced, but exact string of what *would* be
displayed is maintained at all times in the *display* attribute

*transcript* is a filepath to where the status bar should keep a log of
all changes to the display. If *transcript* is None (the default value)
or False, logging is disabled. **WARNING** Using the transcript will
slow down performance by requiring the status bar to make frequent i/o
every time the display is modified. Useful for debugging issues with
prepended or appended text, but not recommended if the transcript is not
needed

-  status\_bar.update(value) updates the display iff *value* would
   require a change in the length of the progress bar, or if it changes
   the percentage readout by at least *update\_threshold*

-  status\_bar.clear(erase=False) Clears the readout from stdout If
   *erase* is true, the readout is cleared entirely Otherwise, the
   cursor position is simply reset to the front of the bar, which will
   overwrite characters in the readout with subsequent output to stdout
   by any source

-  status\_bar.prepend(text) Displays *text* to the left of the bar. It
   will always remain to the left of the bar as the display updates.
   **WARNING** Prepended text offsets the bar. If any part of the bar
   (including prepended or appended text) extends beyond a single line
   on the console, the status bar will not display properly. Prepended
   text should be kept short

-  status\_bar.append(text) Displays *text* to the right of the bar. It
   will always remain to the right of the bar as the display updates.
   **WARNING** Appended text extends the display. If any part of the bar
   (including prepended or appended text) extends beyond a single line
   of the console, the status bar will not display properly. Appended
   text should be kept short

bio.MAF2BED
-----------

The ``agutil.bio.maf2bed`` module provides a command line interface for
converting maf files into bed files To follow the bed format, and to
reduce the size of the bed itself, maf2bed generates two files by
default. A ``.bed`` file with entries in the format of: Chromosome Start
Stop Key and a ``.key`` file with entries in the format of: Key

COMMAND USAGE


-  ``$ maf2bed convert <input> <output> [--exclude-silent] [--skip-keyfile]``
   Converts the file *input* to *output* and *output*.key files. If
   *--exclude-silent* is set, silent mutations are not included in the
   output If *--skip-keyfile* is set, the program only generates a
   single file, *output* which is identical to the *input* file, except
   that start and stop coordinates have been shifted to 0-based

-  ``$ maf2bed lookup <input> <keys...>`` Looks up the entries for each
   key listed in *keys* in the keyfile *input*

bio.TSVMANIP
------------

The ``agutil.tsvManip`` module provides a command line interface for
modifying large tsv files While not *strictly* biology oriented, its
original purpose was to parse and rearrange different fields of bed
files

COMMAND USAGE


-  ``$ tsvmanip <input> <output> [--no-headers] [-c COLUMN] [-d DELIMITER] [--i0 COL] [-s COL] [-m IN:OUT] [-v]``

Parses *input* according to the following arguments, and writes to
*output*

Optional arguments:

*--no-headers* Flag indicating that there are is no header row

*-c COLUMN, --col COLUMN* Column containing input data to parse
(0-indexed). Multiple columns can be selected by providing the option
multiple times (Ex: --col 0 --col 5 --col 6). All columns are selected
by default

*-d DELIMITER, --delim DELIMITER* Delimiters for splitting input columns
into multiple new columns for output Delimiters can be specified for
multiple columns by providing the option multiple times Delimiters are
matched to colums by order provided. For example, the first delimiter
provided matches to the first column parsed for input. An underscore
(\_) indicates no delimiter for that column. To use a delimiter
consisting entirely of one or more underscores, append a single
underscore to the end of the delimiter string. (Ex: '--delim \_\_' (two
underscores) indicates a delimiter of '\_' (one underscore) ). Multiple
delimiters can be provided for the same column by prefixing the
delimiters for the string with : Delimiters for the same column are
applied in the order provided to all resulting columns from subsequent
splits. Prefixed delimiter inputs will not affect the matching of
unprefixed delimiters to columns. (Ex: --col 0 --col 1 --delim --delim )
(Ex: --col 1 --col 4 --delim --delim --delim 1:)

*--i0 COL* Selected columns should be shifted from 1 to 0 index. This is
applied after selected columns are plucked from the input, and split by
delimiters. Provided column numbers match the indecies of columns after
those steps. Multiple columns can be selected by supplying the argument
multiple times

*-s COL, --strip-commas COL* Strip commas from the specified columns.
Column numbers reference before mapping, but after splitting

*-m IN:OUT, --map IN:OUT* Mappings to map plucked columns to output
columns. Use to change the order of columns. Maps are in the format of:
<input column #>:<output column #> This is the last step in parsing, so
input column #'s should be relative to any changes made by plucking and
splitting

*-v* Provide verbose output

.. |Master Build Status| image:: https://travis-ci.org/agraubert/agutil.svg?branch=master
   :target: https://travis-ci.org/agraubert/agutil
.. |Dev Build Status| image:: https://travis-ci.org/agraubert/agutil.svg?branch=dev
   :target: https://travis-ci.org/agraubert/agutil


