==========================
`guix-import-debian`
==========================

---------------------------------------------------------------------
Helper for converting Debian packages into Guix package definitions
---------------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@crazy-compiler.com>
:Version: 0.1
:Copyright: GNU Public License v3 (GPLv3)
:Homepage: https://gitlab.com/htgoebel/guix-import-debian


`guix-import-debian` reads the Debian package description and
``.debian.tar.gz`` from the debian package servers and creates a
(hopefully useful) Guix package definition. Of course, this definition
needs to be reworked to make everything fine for committing to the
Guix project.

This basically saves you some typing and collecting data. it does not
doe the remaining work for you.

Typically things to to are:

- check the source definitons
- check the inputs and native-inputs
- check the synopsis and description
- check the outputs
- test if building works as expected
- run guix lint
- and all the other

The downloaded debian file for this package can be found in $TMP (may
be changed using option ``--tempdir``), so you can easily continue
your research.


Requirements and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Please note: This package is meant for developers, thus installations
  instructions are meant for developers.

`guix-import-debian` requires

* `Python`__ 3.4 or higher (tested with Python 3.4)
* `python-debian`__
* `numconv`__

__ http://www.python.org/download/
__ http://pypi.python.org/pypi/python-debian
__ http://pypi.python.org/pypi/numconv


Installing `guix-import-debian`
---------------------------------

`guix-import-debian` is listed on `PyPI (Python Package Index)`__, so
you can install it using `pip install guix-import-debian` as usual. Please
refer to the manuals of `pip` for further information.

__ http://pypi.python.org/pypi


.. Emacs config:
 Local Variables:
 mode: rst
 ispell-local-dictionary: "american"
 End:
