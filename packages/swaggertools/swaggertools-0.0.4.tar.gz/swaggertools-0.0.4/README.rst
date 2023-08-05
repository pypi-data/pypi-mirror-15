Swagger tools
=============


This library allows you to merge a many file swagger specification into a
single one.


Quick start
-----------

For example, these two files::

    # swagger.yml
    /paths:
      /users: {$ref: grafts/users.yml#/resources/collection}

    # grafts/users.yml
    /resources:
      collection:
        get:
          200:
        post:
          201:


Will be merged as::

    # swagger.yml
    /paths:
      /users:
        get:
          200:
        post:
          201:

Wich can be used to validate your API against `editor.swagger.io <http://editor.swagger.io>`_.


Installation
------------

::

    pip install swaggertools


Usage
-----

As a command line::

    swagger-tools /path/to/swagger.yml


Into python script::

    from swaggertools import resolve

    with open('/path/to/swagger.yml') as filehandler:
        app = resolve(filehandler)
    print(app.to_yaml())
