
Straighter is a program for manipulating straight line programs.

Straighter can be run as a Python 2, Python 3 or `Sage Python
<http://www.sagemath.org/>`_ module. For even more speed (~25% more)
consider running straighter with the -O optimise bytecode option.

Installation
============

`Straighter <https://pypi.python.org/straighter>`_ is available on the `Python Package
Index <https://pypi.python.org>`_. The preferred method for installing the latest
stable release is to use `pip <http://pip.readthedocs.org/en/latest/installing.html>`_
(included in Python 2.7.9 and Python 3.4 by default)::

	> python -m pip install straighter --user --upgrade

.. warning:: As of Sage 6.9, Sage no longer appears to load packages from the user directory.
	Therefore users may need to either install straighter directly into Sage (which may require
	superuser privileges) or add the path to straighter to their SAGE_PATH environment variable.

Usage
=====

Once installed, import straighter by using::

	> import straighter

Citing
======

If you find straighter useful in your research, please consider citing it. A suggested
reference is::

	Mark Bell. straighter (Computer Software).
	pypi.python.org/pypi/straighter, 2016. Version <<version number>>

the BibTeX entry::

	@Misc{straighter,
		author = {Bell, Mark},
		title = {straighter (Computer Software)},
		howpublished = {\url{pypi.python.org/pypi/straighter}},
		year = {2016},
		note = {Version <<version number>>}
	}

or the BibItem::

	\bibitem{straighter} Mark Bell: \emph{straighter (Computer Software)},
		\url{pypi.python.org/pypi/straighter}, (2016),
		Version <<version number>>.

Development
===========

The latest development version of straighter is available from
`BitBucket <https://bitbucket.org/Mark_Bell/straighter>`_.
Alternatively, you can clone the mercurial repository directly using
the command::

	> hg clone https://bitbucket.org/mark_bell/straighter

And then install using the command::

	> python setup.py install --user

