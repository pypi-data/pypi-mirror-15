nose-long-descriptions
======================

.. image:: https://img.shields.io/pypi/v/nose-enhanced-descriptions.svg
    :target: https://pypi.python.org/pypi/nose-enhanced-descriptions
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/paul-butcher/nose_enhanced_descriptions.png
   :target: https://travis-ci.org/paul-butcher/nose_enhanced_descriptions
   :alt: Latest Travis CI build status

A nose plugin to improve nose test description output.  This plugin deals with two problems in the default verbose nose output.   Finding out which test failed, and selectively rerunning tests.

By default, running nosetests verbosely will describe each test with one of

* An id derived from the name and module of the test
* The first line of the docstring

thus::

    I have a docstring ... ok
    test_with_blank_docstring (meta_tests.MetaTest) ... ok
    I have a docstring ... ok
    test_without_docstring (meta_tests.MetaTest) ... ok

If you have multiple tests in different suites with the same or similar docstrings, and one of them fails, it can be difficult to find out which is which.

The description derived from the name of the test is also frustrating.  The format of a command line argument to run a specific test in nose is ``module:TestClass.testmethod``, yet the format of the description is ``testmethod (module.TestClass)``, meaning that the user must construct this argument by copying the various sections into the right place and replacing one of the dots with a colon. 

Usage
-----
``nosetests --verbose --with-enhanced-descriptions``
::

    meta_tests:MetaTest.test_docstring_leading_line
    	(The first line was empty, but this is the line to use.) ... ok
    meta_tests:MetaTest.test_with_blank_docstring ... ok
    meta_tests:MetaTest.test_with_docstring
    	(I have a docstring) ... ok
    meta_tests:MetaTest.test_without_docstring ... ok

The reader can see both the identifier (so that they know exactly which test fails), and the documentation (so that they know what it was supposed to do).  The test identifiers can alo now be copied and run,  e.g. ``nosetests meta_tests:MetaTest.test_without_docstring``.

Installation
------------

``pip install nose_enhanced_descriptions``


Licence
-------

MIT