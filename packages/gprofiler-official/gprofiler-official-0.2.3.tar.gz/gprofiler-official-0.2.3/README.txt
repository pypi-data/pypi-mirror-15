
gprofiler-official
==================

The official Python interface to the g:Profiler [1] toolkit for enrichment
analysis of functional (GO and other) terms, conversion between identifier
namespaces and mapping orhologous genes in related organisms. This library
provides both a command-line tool and a Python module. It is designed to be
lightweight and not require any 3rd party packages.

Besides this README, the API documentation is available [6].

Installation on Linux using pip
-------------------------------

The pip tool [4] is the recommended method of installing Python packages.

Optionally create a virtual environment [2]::

$ virtualenv2 myenv
$ source myenv/bin/activate

Install the software with pip, see [3] for instructions::

$ pip install gprofiler-official

Make sure that the installed gprofiler.py script is on your $PATH. When using
a virtual environment as shown above, this should happen automatically.

Run an example query::

$ gprofiler.py -o scerevisiae "swi4 swi6"

For detailed usage instructions, see::

$ gprofiler.py --help

To use the module in your codebase::

	from gprofiler import GProfiler
	gp = GProfiler("MyToolName/0.1")
	result = gp.gprofile("sox2")

For details, see the API documentation [6].

Installation on Linux using the tarball
---------------------------------------

You may simply download the tarball from gprofiler-official PyPI page [5],
extract it and use the gprofiler.py script without installation. For detailed
usage instructions, see::

$ gprofiler.py --help

You may run the test suite with::

$ python2 setup.py test

Installation on other platforms
-------------------------------

Please see [3] for package installation instructions on various platforms.

* [1] http://biit.cs.ut.ee/gprofiler
* [2] http://docs.python-guide.org/en/latest/dev/virtualenvs/
* [3] https://python-packaging-user-guide.readthedocs.org/en/latest/installing/
* [4] https://pip.pypa.io/en/stable/
* [5] https://pypi.python.org/pypi/gprofiler-official
* [6] http://biit.cs.ut.ee/gprofiler_beta/doc/python/

