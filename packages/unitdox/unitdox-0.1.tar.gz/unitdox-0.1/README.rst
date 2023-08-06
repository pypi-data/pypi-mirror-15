unitdox will output a documentation a human can read based on your python unittests.

.. code-block:: text

    MathTest (sample_tests.math_test)
      test 1 plus 1 equals 2
      test sqrt of a negative number raise a ValueError exception

The latest version
===================

You can find the latest version on github

.. code-block:: shell

    git clone git@github.com:FabienArcellier/unitdox.git

Code Example
===============

It takes a python module as input.

.. code-block:: shell

  python -m unitdox sample_tests

You must see this output

.. code-block:: text

  MathTest (sample_tests.math_test)
	test 1 plus 1 equals 2
	test sqrt of a negative number raise a ValueError exception

Motivation
===========

This script is inspired from the feature testdox on phpunit.
https://phpunit.de/manual/current/en/other-uses-for-tests.html

Installation
=============

You can setup the project with pip. The package is not on PyPi yet.

.. code-block:: shell

  pip install .

After the install, you can use like this :

.. code-block:: shell

  unitdox sample_tests

Tests
======

There is not unit tests yet.

You can check the code consistancy with :

.. code-block:: shell

  make lint

Contributors
=============

* Fabien Arcellier

License
========

.. code-block:: text

  Copyright (c) 1998, Regents of the University of California
  All rights reserved.
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
  * Neither the name of the University of California, Berkeley nor the
  names of its contributors may be used to endorse or promote products
  derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
