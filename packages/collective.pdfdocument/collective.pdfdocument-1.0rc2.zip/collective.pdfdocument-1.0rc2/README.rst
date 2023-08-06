.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.pdfdocument
==============================================================================

.. image:: https://travis-ci.org/collective/collective.pdfdocument.svg?branch=master
    :target: https://travis-ci.org/collective/collective.pdfdocument

This package provides PDF metadata extraction and cover image generation
for Plone. Please see the collective.filemeta package for more information
(at github or PyPI).

Features
---------

- PDF metadata extraction
- PDF cover page PNG generation

Installation
------------

Install collective.pdfdocument by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.pdfdocument


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.pdfdocument/issues
- Source Code: https://github.com/collective/collective.pdfdocument


Support
-------

If you are having issues, please let us know.

License
-------

The project is licensed under the GPLv2.
