=========================
Poort: The quick gateway.
=========================

.. image:: https://coveralls.io/repos/github/CorverDevelopment/Poort/badge.svg?branch=master
   :target: https://coveralls.io/github/CorverDevelopment/Poort?branch=master
   :alt: Coverage

.. begin

Poort is a bundle of best-practices to quickly build web gateways.

* Free software: MIT license
* Documentation: http://pythonhosted.org/poort

A quick example::

    # -*- coding: utf-8 -*-
    from __future__ import absolute_import, division, print_function

    from poort import Gate, Request, Response

    gate = Gate()

    def application(environ, start_response):
        with gate(environ):
            request = gate.request

            if request.path == '/':
                response = Response('Hallo world!')
            else:
                response = Response('Whoops, not found.', status=404)

            return response(request, start_response)

Features
--------

- Gate, which provides a simple getter/setter interface for local variables.
- Request, a very simple object containing all the information about the request.
- Response, a versatile but simple object that can respond to the requester.

Authors
-------

``Poort`` is written and maintained by
`Nils Corver <nils@corverdevelopment.nl>`_.

A full list of contributors can be found in
`GitHub's overview <https://github.com/corverdevelopment/poort/graphs/contributors>`_.
