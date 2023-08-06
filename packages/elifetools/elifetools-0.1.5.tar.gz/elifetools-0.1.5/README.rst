elife-tools
===========

.. image:: https://travis-ci.org/elifesciences/elife-tools.svg?branch=master
   :target: https://travis-ci.org/elifesciences/elife-tools
   :alt: Latest Version
   
.. image:: https://coveralls.io/repos/elifesciences/elife-tools/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/elifesciences/elife-tools?branch=master

Tools for using article data in Python

Non-Python dependencies
=======================

* libxml2 (Ubuntu, Arch)

Install for users
=================

Install via `pip <http://www.pip-installer.org/>`_:

.. code-block:: bash

   $ pip install elifetools
   
You might need to install libxml manually first

.. code-block:: bash

   $ sudo STATIC_DEPS=true pip install lxml==3.4.1

To install the latest version directly from git

.. code-block:: bash

   $ pip install git+https://github.com/elifesciences/elife-tools.git@master

or you can add it to your project's requirements.txt file

.. code-block:: bash

   git+https://github.com/elifesciences/elife-tools.git@master


Install for developers
======================

Clone the git repo

Make a virtualenv (optional)

Then

.. code-block:: bash

   $ python setup.py install

Example usage
=============

.. code-block:: python

    >>> from elifetools import parseJATS as parser
    >>> soup = parser.parse_document('sample-xml/elife-kitchen-sink.xml')
    >>> print parser.doi(soup)

More code examples can be found in `tests/unittests/basic_usage_test.py`

These code examples can be run with:

.. code-block:: bash

    $ cd elifetools/
    $ python -m unittest discover -s tests/unittests/ -p *_test.py

and with xml output:

.. code-block:: bash

    $ cd elifetools/
    $ python -m xmlrunner discover -s tests/unittests/ -p *_test.py

Testing
=======

`Lettuce <http://packages.python.org/lettuce/>`_ for testing.

.. code-block:: bash

   $ cd elifetools/tests
   $ lettuce
   
License
=========

`The MIT License <http://opensource.org/licenses/mit-license.php>`_
