Run a client
============

Clients declare federated datasets that are comprised by multiple
data fragments scattered across multiple servers. A client needs
to first declare a dataset comprising multiple such fragments.
Then, the dataset can be treated as a standalone object on which
operations can be performed as long as all dependent servers are
up and running. Similarly to servers, clients require some
configuration to know which operations are available to them and
how they may be performed.

Configuration
-------------

Configuration files have a format that allows you to share
the same ones between clients and servers if convenient,
where each reads from the respective segment.
Find a first default that you can edit here
:ref:`here <https://github.com/maniospas/FedMed/blob/main/example/config.yaml>`.
Clients only need to know about non-reduce methods that
they can call. They are allowed to try to call even
methods that servers do not support, although in this
case they will receive back an error message and computations
will not finish.

That said, you will typically find it useful to use this
default configuration everywhere, as it is up to date with
all available operations implemented within *FedMed*.
More details on
configuration files can be found :doc:`here <../config/mapreduce>`.

Connecting to data fragments
----------------------------

Set up communication channels with remote data fragments
(i.e., parts of the same dataset) and organize them into
one dataset. Fragments in the same dataset may match only partially
in terms of structure, as access to them relies
on duck-typing. More details on the format data may have
can be found :doc:`here <../basics/data>`. For the time being, let
us see how a dataset that combines data fragments
looks like:

.. code-block:: python

    import fedmed as fm
    sources = [
        fm.Remote(ip="http://127.0.0.1:8000", fragment="test array part 1"),
        fm.Remote(ip="http://127.0.0.1:8000", fragment="test array part 2")
    ]
    data = fm.FedData(sources, config="config.yaml")

Performing operations
---------------------

Call simple operations among those described in the configuration
file, stored in `config.yaml` in the above snippet.
Find a first default that you can edit
:ref:`here <https://github.com/maniospas/FedMed/blob/main/example/config.yaml>`.
The same file could be shared between the client and servers,
but this is not mandatory; some servers may not support some
of these capabilities, in which case you will fail dependent
computations you will try to run.

Operations are performed under a map-reduce scheme.
The map runs in the servers, and the reduce on the client.
Each server is left in control of both how it performs its
namesake map methods, and how it distorts outcomes to comply
with some privacy policy.

.. code-block:: python

    mean = data.sum() / data.len()
    print('Mean', mean)

.. warning:: Control of map operations allows server owners to
    set their own privacy policies. This means that there is
    no guarantee about exact data computation on your end.

For the above code to run, you need to set up some devices to run at the respective IP addresses.
