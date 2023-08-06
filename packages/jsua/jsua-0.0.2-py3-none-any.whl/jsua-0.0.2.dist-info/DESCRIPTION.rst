jsua
====

|License| |PyPI| |CircleCI|

jsua, pronounced Joshua, is a streaming sax-like parser for JSON files.
It's special because it doesn't require you to start at the beginning of
a JSON stream. You can start anywhere, and it will eventually start
spitting out events.

Usage
-----

.. code:: python

    from jsua import SynchronizingParser
    from io import StringIO

    json = StringIO('{"hello": "world"}')
    parser = SynchronizingParser(json)

    for state, event, value in parser.parse():
        print(state, event, value)

.. |License| image:: https://img.shields.io/badge/license-LGPL-blue.svg
.. |PyPI| image:: https://img.shields.io/pypi/v/jsua.svg?maxAge=86400
.. |CircleCI| image:: https://img.shields.io/circleci/project/tecywiz121/jsua.svg?maxAge=86400


