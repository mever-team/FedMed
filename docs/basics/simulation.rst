Run locally
===========

FedMed offers two data sources that can incorporate
local data, i.e., loaded from within the client machine:
a) a production-ready `Local` data source, which creates
minimal overhead, and b) a scalable `Simulation` data source,
which wraps calls to a programmatically declared server without needing
to start a Flask service on an IP and can be used as proof-of-concept.

Local data
----------

You can create datasets by combining data fragments.
The format data may vary (duck typing is supported)
and the common principles are described
:doc:`here <../basics/data>`. For the time being,
consider simple data fragments where each entry
corresponds to a data sample. You can create `Local`
data sources and combine them (think of this as
a concatenation along the data sample direction) like this:

.. code-block:: python

    import fedmed as fm
    sources = [
        fm.Local([1, 2, 3, 4]),
        fm.Local([5, 6, 7, 8, 9]),
    ]

    data = fm.FedData(sources, config="config.yaml")

Local data sources do *not* apply any privacy policies and
therefore perform exact computations. To simulate that outcome
of running servers see below. Below we show an example of how
`FedData` instances can be involved in operations, given
that the later are supported by both clients and servers - in the
simplest cases they will be, but read more on configuration
:doc:`here <../config/mapreduce>`. *FedMed* provides
several common data analysis
:doc:`operations <../operations/operations>` and
:doc:`statistical tests <../operations/tests>`.


.. code-block:: python

    from fedmed.stats import sum, len
    msq = sum(data**2) / len(data)
    print("MSQ", msq)


Scalable simulation
-------------------

To create a simulation of a would-be scenario without the cost
of running multiple services, you can use a `Simulation` data
source. This requires :doc:`setting up servers <../basics/server>`,
with its own configuration. Here is an example, where there is only
one data fragment `"testA"` per server and the same file
is used to configure both of them. You can
extend this example to show proof-of-concept in one machine:

.. code-block:: python

    import fedmed as fm
    server1 = fm.Server(config="config.yaml")
    server2 = fm.Server(config="config.yaml")
    server1["testA"] = [1, 2, 3, 4]  # or dict of lists, pandas dataframe, etc
    server2["testA"] = [5, 6, 7, 8, 9]

You can now add the servers within a Simulation data source that
references which fragment should be obtained from each one:

.. code-block:: python

    sources = [
        fm.Simulation(server1, "testA"),
        fm.Simulation(server2, "testA"),
    ]

    data = fm.FedData(sources, config="config.yaml")

Server simulations will also perform
json serialization and serialization
that occurs during data transfers (it only removes the
data structure element).

You can set a custom communication
layer in the simulation that helps you gather statistics
about data usage when the proof-of-concept will be applied
in practice. You can have a different communication layer
for each simulated server, or use the same one to
get a sense of data transmitted and received by the client
application. This can be done like this:


.. code-block:: python

    communication = fm.SimulatedCommunication(tracker=True)
    sources = [
        fm.Simulation(server=server1, fragment="testA", communication=communication),
        fm.Simulation(server=server1, fragment="testB", communication=communication)
    ]

    data = fm.FedData(sources, config="config.yaml")
    print(sum(data**2)/len(data))

    import numpy as np
    print("Total sent bytes", np.array(communication.sent).sum())
    print("Total received bytes", np.array(communication.received).sum())




