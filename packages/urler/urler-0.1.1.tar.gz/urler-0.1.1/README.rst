===============================
URLer - GET it?
===============================

.. image:: https://img.shields.io/pypi/v/urler.svg
        :target: https://pypi.python.org/pypi/urler

.. image:: https://img.shields.io/travis/kintoandar/urler.svg
        :target: https://travis-ci.org/kintoandar/urler

.. image:: https://readthedocs.org/projects/urler/badge/?version=latest
        :target: https://readthedocs.org/projects/urler/?badge=latest
        :alt: Documentation Status



* Free software: MIT license
* Documentation: https://urler.readthedocs.org.

About
-----

``urler`` is a simple script to GET an URL or a ``.csv`` list of URLs.

Install
-------

``pip install urler``

How To
------

.. code:: bash

    URLer

    Usage:
        urler (<host> <port> <path> | <file>)
        urler (-h | --help | --version)

    Examples:
        urler example.com 8080 index.html
        urler targets.csv

    Assumptions:
        you know what you are doing

    Commands:
        host         target host
        port         destination port
        path         URL path
        file         system path to a csv file with the following fields: host,port,path

    Options:
        -h, --help    show this help message and exit
        --version     prints program version and exit
