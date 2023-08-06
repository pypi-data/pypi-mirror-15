===============================
Pykemon
===============================

.. image:: https://badge.fury.io/py/pykemon.png
    :target: http://badge.fury.io/py/pykemon

.. image:: https://travis-ci.org/PokeAPI/pykemon.png?branch=master
        :target: https://travis-ci.org/PokeAPI/pykemon

A python wrapper for `PokeAPI <http://pokeapi.co>`_

* Free software: BSD license
* Documentation: http://pykemon.rtfd.org.


Installation
------------

Nice and simple:

.. code-block:: bash

    $ pip install pykemon


Usage
-----

Even simpler:

.. code-block:: python

    >>> import pykemon
    >>> client = pykemon.V1Client()
    >>> p = client.get_pokemon(uid=1)
    [<Pokemon - Bulbasaur>]


Features
--------

* Generate Python objects from PokeAPI resources.

* Human-friendly API




History
-------

0.2.0 (2016-06-11)
++++++++++++++++++

* Beckett API Client framework added

0.1.2 (2014-1-3)
++++++++++++++++++

* Sprite attribute added to Pokemon class


0.1.1 (2013-12-24)
++++++++++++++++++

* Description attribute added to Pokemon class


0.1.0 (2013-12-23)
++++++++++++++++++

* First release on PyPI.
* All PokeAPI resources fully supported and represented in an object-oriented style.
* Easy-to-use API: just one method!


