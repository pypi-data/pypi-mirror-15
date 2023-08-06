
Fatter is a program for manipulating fat graphs.

Fatter can be run as a Python 2, Python 3 or `Sage Python
<http://www.sagemath.org/>`_ module. For even more speed (~25% more)
consider running fatter with the -O optimise bytecode option.

Installation
============

`Fatter <https://pypi.python.org/fatter>`_ is available on the `Python Package
Index <https://pypi.python.org>`_. The preferred method for installing the latest
stable release is to use `pip <http://pip.readthedocs.org/en/latest/installing.html>`_
(included in Python 2.7.9 and Python 3.4 by default)::

	> python -m pip install fatter --user --upgrade

.. warning:: In order to use the fatter GUI on OS X, users must first update
	their copy of Tk/Tcl as described `here <https://www.python.org/download/mac/tcltk/>`_.
	Flipper has been tested with `ActiveTcl 8.5.18 <http://www.activestate.com/activetcl/downloads>`_.
	Additionally, if running under fatter Sage, users must then reinstall sage python
	by using the command::

	> sage -f python

.. warning:: As of Sage 6.9, Sage no longer appears to load packages from the user directory.
	Therefore users may need to either install fatter directly into Sage (which may require
	superuser privileges) or add the path to fatter to their SAGE_PATH environment variable.

Usage
=====

Once installed, start the fatter GUI by using::

	> python -m fatter.app

Citing
======

If you find fatter useful in your research, please consider citing it. A suggested
reference is::

	Mark Bell. fatter (Computer Software).
	pypi.python.org/pypi/fatter, 2016. Version <<version number>>

the BibTeX entry::

	@Misc{fatter,
		author = {Bell, Mark},
		title = {fatter (Computer Software)},
		howpublished = {\url{pypi.python.org/pypi/fatter}},
		year = {2016},
		note = {Version <<version number>>}
	}

or the BibItem::

	\bibitem{fatter} Mark Bell: \emph{fatter (Computer Software)},
		\url{pypi.python.org/pypi/fatter}, (2016),
		Version <<version number>>.

Development
===========

The latest development version of fatter is available from
`BitBucket <https://bitbucket.org/Mark_Bell/fatter>`_.
Alternatively, you can clone the mercurial repository directly using
the command::

	> hg clone https://bitbucket.org/mark_bell/fatter

And then install using the command::

	> python setup.py install --user

