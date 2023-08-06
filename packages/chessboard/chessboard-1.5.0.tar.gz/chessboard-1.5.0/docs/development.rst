Development
===========


Philosophy
----------

1. First create something that work (to provide business value).
2. Then something that's beautiful (to lower maintenance costs).
3. Finally works on performance (to avoid wasting time on premature
   optimizations).


Build status
------------

==============  ==================  ===================
Branch          |master-branch|__   |develop-branch|__
==============  ==================  ===================
Unittests       |build-stable|      |build-dev|
Coverage        |coverage-stable|   |coverage-dev|
Quality         |quality-stable|    |quality-dev|
Dependencies    |deps-stable|       |deps-dev|
Documentation   |docs-stable|       |docs-dev|
==============  ==================  ===================

.. |master-branch| replace::
   ``master``
__ https://github.com/kdeldycke/chessboard/tree/master
.. |develop-branch| replace::
   ``develop``
__ https://github.com/kdeldycke/chessboard/tree/develop

.. |build-stable| image:: https://img.shields.io/travis/kdeldycke/chessboard/master.svg?style=flat
    :target: https://travis-ci.org/kdeldycke/chessboard
    :alt: Unit-tests status
.. |build-dev| image:: https://img.shields.io/travis/kdeldycke/chessboard/master.svg?style=flat
    :target: https://travis-ci.org/kdeldycke/chessboard
    :alt: Unit-tests status

.. |coverage-stable| image:: https://codecov.io/github/kdeldycke/chessboard/coverage.svg?branch=master
    :target: https://codecov.io/gh/kdeldycke/chessboard/branch/master
    :alt: Coverage Status
.. |coverage-dev| image:: https://codecov.io/github/kdeldycke/chessboard/coverage.svg?branch=develop
    :target: https://codecov.io/gh/kdeldycke/chessboard/branch/develop
    :alt: Coverage Status

.. |quality-stable| image:: https://img.shields.io/scrutinizer/g/kdeldycke/chessboard.svg?style=flat
    :target: https://scrutinizer-ci.com/g/kdeldycke/chessboard/?branch=master
    :alt: Code Quality
.. |quality-dev| image:: https://img.shields.io/scrutinizer/g/kdeldycke/chessboard.svg?style=flat
    :target: https://scrutinizer-ci.com/g/kdeldycke/chessboard/?branch=develop
    :alt: Code Quality

.. |deps-stable| image:: https://img.shields.io/requires/github/kdeldycke/chessboard/master.svg?style=flat
    :target: https://requires.io/github/kdeldycke/chessboard/requirements/?branch=master
    :alt: Requirements freshness
.. |deps-dev| image:: https://img.shields.io/requires/github/kdeldycke/chessboard/develop.svg?style=flat
    :target: https://requires.io/github/kdeldycke/chessboard/requirements/?branch=develop
    :alt: Requirements freshness

.. |docs-stable| image:: https://readthedocs.org/projects/chessboard/badge/?version=stable
    :target: http://chessboard.readthedocs.io/en/stable/
    :alt: Documentation Status
.. |docs-dev| image:: https://readthedocs.org/projects/chessboard/badge/?version=develop
    :target: http://chessboard.readthedocs.io/en/develop/
    :alt: Documentation Status


Setup a development environment
-------------------------------

Check out latest development branch:

.. code-block:: bash

    $ git clone git@github.com:kdeldycke/chessboard.git
    $ cd ./chessboard
    $ git checkout develop

Install package in editable mode with all development dependencies:

.. code-block:: bash

    $ pip install -e .[develop]

Now you're ready to hack and abuse git!


Unit-tests
----------

Install test dependencies and run unit-tests:

.. code-block:: bash

    $ pip install -e .[tests]
    $ nosetests


Coding style
------------

Run `isort <https://pep8.readthedocs.org>`_ utility to sort Python imports:

.. code-block:: bash

    $ pip install -e .[develop]
    $ isort --apply

Then run `PEP8 <https://pep8.readthedocs.org>`_ and `Pylint
<http://docs.pylint.org>`_ code style checks:

.. code-block:: bash

    $ pip install -e .[develop]
    $ pep8 chessboard
    $ pylint --rcfile=setup.cfg chessboard


Build documentation
-------------------

The documentation you're currently reading can be built locally with `Sphinx
<http://www.sphinx-doc.org>`_:

.. code-block:: bash

    $ pip install -e .[docs]
    $ sphinx-apidoc -f -o ./docs .
    $ sphinx-build -b html ./docs ./docs/html


Release process
---------------

Start from the ``develop`` branch:

.. code-block:: bash

    $ git clone git@github.com:kdeldycke/chessboard.git
    $ cd ./chessboard
    $ git checkout develop

Install development dependencies:

.. code-block:: bash

    $ pip install -e .[develop]

Revision should already be set to the next version, so we just need to set the
released date in the changelog:

.. code-block:: bash

    $ vi ./CHANGES.rst

Create a release commit, tag it and merge it back to ``master`` branch:

.. code-block:: bash

    $ git add ./chessboard/__init__.py ./CHANGES.rst
    $ git commit -m "Release vX.Y.Z"
    $ git tag "vX.Y.Z"
    $ git push
    $ git push --tags
    $ git checkout master
    $ git pull
    $ git merge "vX.Y.Z"
    $ git push

Push packaging to the `test cheeseshop
<https://wiki.python.org/moin/TestPyPI>`_:

.. code-block:: bash

    $ python ./setup.py register -r testpypi
    $ python ./setup.py clean
    $ rm -rf ./build ./dist
    $ python ./setup.py sdist bdist_egg bdist_wheel upload -r testpypi

Publish packaging to `PyPi <https://pypi.python.org>`_:

.. code-block:: bash

    $ python ./setup.py register -r pypi
    $ python ./setup.py clean
    $ rm -rf ./build ./dist
    $ python ./setup.py sdist bdist_egg bdist_wheel upload -r pypi

Update revision with `bumpversion <https://github.com/peritus/bumpversion>`_
and set it back to development state by increasing the ``patch`` level.

.. code-block:: bash

    $ git checkout develop
    $ bumpversion --verbose patch
    $ git add ./chessboard/__init__.py ./CHANGES.rst
    $ git commit -m "Post release version bump."
    $ git push

Now if the next revision is no longer bug-fix only, bump the ``minor``
revision level instead:

.. code-block:: bash

    $ bumpversion --verbose minor
    $ git add ./chessboard/__init__.py ./CHANGES.rst
    $ git commit -m "Next release no longer bug-fix only. Bump revision."
    $ git push
