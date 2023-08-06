=======================
Esc: Expect Status Code
=======================

Checks your HTTP response has the expected status, throws an error if not:

.. code:: python

  >>> response = esc.expect(404, requests.get("http://example.com"))
  esc.UnexpectedStatusCode: Expected one of HTTP 404, but http://example.com/ returned 200 with content: <!doctype html>


Why?
====

1. Status code checks are ever so slightly easier.
2. Unit test failure messages are far more helpful.


Supported libraries
===================

Currently supports the following:

- requests
