Remote operations
=================

Map-reduce schema
-----------------

When retrieving aggregate information from servers,
a map-reduce computational model is employed.
In this, each server computes its own information
based on local data and sends it to the client for
further reduction across servers. Correctness is
based on the premise that server functionality
is performed as advertised by the requested operations,
barring small errors induced from maintaining
:doc:`security <privacy>`.

Map-reduce operations are declared under the `methods`
segment of your configuration and differs between
clients and servers; clients declare the reduce function
to be applied on public data, whereas servers declare
the map function to run on their local private data.
The methods are referenced from their importable path.
You can create one common configuration file to share
between clients and servers, where each one reads
the appropriate (`map` or `reduce`) property. This
configuration will look like this:

.. code-block:: yaml

    # ... other configuration
    methods:
      # ... other operations
      max:
        map: fedmed.ops.private.max
        reduce: fedmed.ops.public.max
      len:
        map: fedmed.ops.private.num
        reduce: fedmed.ops.public.sum

Pure remote operations
----------------------


Client configuration
--------------------

Common operations available for client reduction mechanisms
may be found in the `fedmed.ops.public` module, and take
the form of processing lists of server outputs, where
None values denote server-side errors (e.g., unsupported
namesake map function) and should be ignored.
Servers are not required to disclose all errors.

.. note:: You can write your own versions of reduction mechanisms.

Excluding the server part, typically client methods.
Calling the whole map-reduce scheme can be done either
via a functional call on `FedData` objects or by declaring
a `Remote` callable. The following snippet demonstrates
these two patterns:

.. code-block:: python

    import fedmed as fm

    config_file = "config.yaml"
    data = FedData(sources=..., config=config_file)

    # functional call
    mean = data.sum() / data.len()
    print('Mean', mean)

    # procedural call (declare the methods first)
    sum = RemoteRunnable("sum")
    len = RemoteRunnable("len")
    mean = sum(data) / len(data)
    print('Mean', mean)


.. note:: Some FedMed modules depend on :doc:`base numerical
    analysis operations <../operations/operations>` that
    are set as remote runnables, like above. The availability
    of such operations is determined by client and server
    configuration.


Server configuration
--------------------

This describes common operations available to clients.

In addition to reductions, servers may also expose internal
methods
