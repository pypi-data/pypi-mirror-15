💫 Beckett
-------

_Hypermedia API Client Framework_

[![PyPi][pypi-image]][pypi-link]
[![PyPi downloads][pypi-dl-image]][pypi-link]
[![CircleCI][circle-image]][circle-link]
[![Coverage Status][codecov-image]][codecov-link]

![quantumleap](docs/media/leap.gif)

Beckett is a convention-based framework for building Python interfaces around HTTP APIs.

📚 [Documentation](https://phalt.github.io/beckett)
----

📖 Features
--------

* Define your Beckett client in Python instead of a data serialization language.
* Encourages good HTTP and REST practices without being too strict.
* Resources are transformed into typed instances - no more raw dictionaries!
* Automatic URL routing for RESTful interaction to your resources.
* SSL, rate limiting, timeout, and HTTP handling.
* Hypermedia relationship links are automagically resolved into python methods.
* Supports hypermedia response formats such as JSONAPI and HAL.
* Works out of the box, but each resource is completely configurable.


🎥 Credits
---------

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter).

We use [Python Requests](http://docs.python-requests.org/en/master/) for talking HTTP.

Free software: [ISC license](https://github.com/phalt/beckett/blob/master/LICENSE)


[pypi-image]: https://img.shields.io/pypi/v/beckett.svg
[pypi-link]: https://pypi.python.org/pypi/beckett
[pypi-dl-image]: https://img.shields.io/pypi/dm/beckett.png
[circle-image]: https://circleci.com/gh/phalt/beckett/tree/master.svg?style=svg
[circle-link]: https://circleci.com/gh/phalt/beckett/tree/master
[codecov-image]: https://codecov.io/gh/phalt/beckett/branch/master/graph/badge.svg?token=T9mYPv0Ep2
[codecov-link]: http://codecov.io/github/phalt/beckett?branch=master
