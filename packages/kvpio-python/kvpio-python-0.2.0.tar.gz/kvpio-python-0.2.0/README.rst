

`kvp.io <https://www.kvp.io>`_ is a micro-service designed to empower
automation, in any cloud, in any data-center, with ease.

kvp.io-python
-------------
The python library and cli for `kvp.io <https://www.kvp.io>`_.

Installation
------------
Requires ``requests`` and ``click``.

``pip install kvpio-python``

Tests
-----
Requires ``pytest`` and ``pytest-cov``.

``py.test --cov-report term --cov=kvpio``

CLI Documentation
-----------------
The cli is a simple utility suitable for use by itself or in an automation
pipeline. See the examples section below or get usage help by running:

``kvpio --help``

To be useful, your API key must be provided via one of the following:

- as an environment variable name ``KVPIO_APIKEY``
- as a single line in the file ``~/.kvpio``

API Documentation
-----------------
See `kvp.io-python <https://kvpio.github.io/kvp.io-python-docs>`_ for the API
docs. See the examples section below for more.

CLI Examples
------------
Here are a few examples to get you familiar with the cli.

Basic bucket usage:

.. code:: bash

    $ export KVPIO_APIKEY=<your api key here>
    $ kvpio bucket set foo bar
    $ kvpio bucket get foo
    bar

Bucket with nested data:

.. code:: bash

    $ kvpio bucket set foo '{"bar": {"baz": 123}}'
    $ kvpio bucket get foo/bar/baz
    123

Basic template usage:

.. code:: bash

    $ kvpio template set foo 'baz is equal to {{ foo.bar.baz }}'
    $ kvpio template get foo
    baz is equal to 123

Get account information:

.. code:: bash

    $ kvpio account
    {"id": "kvp.io", "email": "support@kvp.io", "reads": 87, "size": 124}

API Examples
------------
Here are a few examples to get you familiar with the API.

Accessing account information:

.. code:: python

    import kvpio
    kvpio.api_key = '123abc'
    account = kvpio.Account().get()
    # {"id": "kvp.io", "email": "support@kvp.io", "reads": 87, "size": 124}

Writing to your bucket:

.. code:: python

    data = {
        'foo': 123,
        'bar': True,
        'baz': {
            'boo': 321,
            'far': False,
            'faz': [1, 2, 3]
        }
    }
    bucket = kvpio.Bucket()
    bucket.set('my_key', data)

Reading nested data from your bucket:

.. code:: python

    data = bucket.get('my_key/baz/faz')
    # [1, 2, 3]
