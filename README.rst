.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.


.. image:: https://github.com/IMIO/imio.smartweb.core/workflows/Tests/badge.svg
    :target: https://github.com/IMIO/imio.smartweb.core/actions?query=workflow%3ATests
    :alt: CI Status

.. image:: https://coveralls.io/repos/github/IMIO/imio.smartweb.core/badge.svg?branch=main
    :target: https://coveralls.io/github/IMIO/imio.smartweb.core?branch=main
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/imio.smartweb.core.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.core/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/imio.smartweb.core.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.core
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/imio.smartweb.core.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/imio.smartweb.core.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.core/
    :alt: License


==================
imio.smartweb.core
==================

Core product for iMio websites

Features
--------

This products contains:
- Content types: Folder, Page, Procedure, Sections ...
- Behaviors to configure display in menus / navigations and handle sub-sites
- Complete viewlets organization (header, footer) to get rid of portlets

A folder can be transformed into a sub-site, which has its navigation viewlet, a logo viewlet, ...

A page (or procedure) can be defined as default page of a folder, changing the way it appears in menus / breadcrumbs / sitemap.

Pages & Procedures can contain different "sections" (Text, Galery, Video, ...).
Those sections can be styled (bootstrap or custom css classes) and rearranged.

A banner can be defined to be displayed on any folder (& its children) and can be hidden locally on any content.


Examples
--------

Hopefully soon in production :-)


Documentation
-------------

TODO


Translations
------------

This product has been translated into

- French

The translation domain is imio.smartweb domain and the translations are stored in imio.smartweb.locales package.


Known issues
------------

- Dexterity Plone site & multilingual roots are not yet handled.


Installation
------------

Install imio.smartweb.core by adding it to your buildout::

    [buildout]

    ...

    eggs =
        imio.smartweb.core


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/imio/imio.smartweb.core/issues
- Source Code: https://github.com/imio/imio.smartweb.core


License
-------

The project is licensed under the GPLv2.
