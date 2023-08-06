

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Shared follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Shared uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.shared.png?branch=master
  :target: https://travis-ci.org/OneGov/onegov.shared
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.shared/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.shared?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://img.shields.io/pypi/v/onegov.shared.svg
  :target: https://pypi.python.org/pypi/onegov.shared
  :alt: Latest PyPI Release

License
-------
onegov.shared is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~
0.2.0 (2016-06-10)
~~~~~~~~~~~~~~~~~~~

- Supports the new field dependency options of onegov.form.
  [msom]

0.1.0 (2015-10-12)
~~~~~~~~~~~~~~~~~~~

- Removes Python 2.x support.
  [href]

0.0.1 (2015-10-07)
~~~~~~~~~~~~~~~~~~~

- Initial Release


