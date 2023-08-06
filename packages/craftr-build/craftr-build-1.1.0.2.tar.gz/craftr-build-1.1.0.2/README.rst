Craftr
======

|PyPI Version| |Travis CI| |Documentation Status|

Craftr is a next generation build system based on
`Ninja <https://github.com/ninja-build/ninja>`__ and
`Python <https://www.python.org>`__. And don't worry, it isn't like waf
or SCons!

-  `Changelog (latest) <docs/changelog.rst>`__
-  `Documentation (latest) <craftr.readthedocs.io/en/latest/>`__
-  `Documentation (stable) <craftr.readthedocs.io/en/stable/>`__
-  `List of third-party extension
   modules <https://github.com/craftr-build/craftr/wiki/Craftr-Extensions>`__
-  `Projects using
   Craftr <https://github.com/craftr-build/craftr/wiki/Projects-using-Craftr>`__

Contribute
~~~~~~~~~~

I welcome all contributions, feedback and suggestions! If you have any
of those or just want to chat, ping me on
`twitter <https://twitter.com/rosensteinn>`__, by
`mail <mailto:rosensteinniklas@gmail.com>`__ or open a `new
issue <https://github.com/craftr-build/craftr/issues/new>`__!

Requirements
~~~~~~~~~~~~

-  `Ninja <https://github.com/ninja-build/ninja>`__
-  `Python <https://www.python.org>`__ 3.4 or higher
-  see `requirements.txt <requirements.txt>`__
-  `Pandoc <http://pandoc.org>`__ when installing from the Git
   repository

Installation
~~~~~~~~~~~~

::

    pip install craftr-build

To install from the Git repository, use the ``-e`` flag to be able to
update Craftr by simply pulling the latest changes from the remote
repository.

::

    git clone https://github.com/craftr-build/craftr.git && cd craftr
    pip install -e .

--------------

MIT Licensed – Copyright © 2016 Niklas Rosenstein

.. |PyPI Version| image:: https://img.shields.io/pypi/v/craftr-build.svg
   :target: https://pypi.python.org/pypi/craftr-build
.. |Travis CI| image:: https://travis-ci.org/craftr-build/craftr.svg
   :target: https://travis-ci.org/craftr-build/craftr
.. |Documentation Status| image:: https://readthedocs.org/projects/craftr/badge/?version=latest
   :target: http://craftr.readthedocs.io/en/latest/?badge=latest
