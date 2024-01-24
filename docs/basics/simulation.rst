Local run
=========

FedMed offers two data sources that can incorporate
local data, i.e., loaded from within the client machine:
a) a production-ready Local data source, which creates
minimal overhead, and b) a scalable Simulation data source,
which wraps calls to a programmatic Server without needing
to start a Flask service on an IP. The last option offers
a fully scalable simulation, for example to demonstrate
proof-of-concept of privacy policies or new operations
in one machine.

Local production data
---------------------

You may add local data as fragments in your data sources,
for example to run a client within one of your servers with
exact information. You can mix local and remote sources
together with no issue.

.. code-block:: python

    import fedmed as fm
    sources = [
        fm.Local([1, 2, 3, 4, 5, 6, 7, 8]),
        fm.Local([5, 6, 7, 8, 9]),
    ]

    data = fm.FedData(sources, config="config.yaml")

.. note:: Local data sources do *not* apply any privacy policies and therefore perform exact computations. To simulate that outcome of running servers see below.

Scalable proof-of-concept
-------------------------

To create a simulation of a would-be scenario without the cost
of running multiple services, you can use a `Simulation` data
source. This requires :doc:`setting up a server <../basics/server>`
with its own configuration, like usual:

.. code-block:: python

    import fedmed as fm
    server = fm.Server(config="config.yaml")
    data = [1, 2, 3]  # or dict of lists, pandas dataframe, etc
    server["test array part 1"] = data

You can now add the server within a Simulation data source per:

.. code-block:: python

    sources = [
        fm.Simulation(server),
    ]

    data = fm.FedData(sources, config="config.yaml")

.. note:: You may simulate multiple servers at the same time,
    each with a different privacy policy.

.. warning:: Running server simulations may require intensive
    operations, including json serialization and serialization
    that occurs during data transfers (it only removes the
    data structure element).
