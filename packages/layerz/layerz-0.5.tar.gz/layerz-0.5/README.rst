Layerz
======

A simple module for creating layers of dependencies.

Installation
------------

Just use pip!::

    $ pip install layerz

Usage
-----

.. code-block:: python

    from layerz import Layers

    dep1 = type("dep1", (object, ), {"dependencies": lambda s, all_deps: []})()
    dep2 = type("dep2", (object, ), {"dependencies": lambda s, all_deps: ["dep3"]})()
    dep3 = type("dep3", (object, ), {"dependencies": lambda s, all_deps: ["dep1"]})()
    dep4 = type("dep4", (object, ), {"dependencies": lambda s, all_deps: ["dep3"]})()
    dep5 = type("dep1", (object, ), {"dependencies": lambda s, all_deps: ["dep4", "dep2"]})()

    layers = Layers({"dep1": dep1, "dep2": dep2, "dep3": dep3, "dep4": dep4, "dep5": dep5})
    layers.add_to_layers("dep5")
    for layer in layers.layered:
        # might get something like
        # [("dep5", dep5)]
        # [("dep4", dep4), ("dep2", dep2)]
        # [("dep3", dep3)]
        # [("dep1", dep1)]

When we create the layers, it will do a depth first addition of all dependencies
and only add a dep to a layer that occurs after all it's dependencies.

Cyclic dependencies will be complained about.

Tests
-----

Install locally::

    $ pip install -e .
    $ pip install -e ".[tests]"

And then use the helper script::

    $ ./test.sh

