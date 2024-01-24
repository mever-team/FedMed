Client setup
============

Connecting to data fragments
----------------------------

Set up communication channels with remote data fragments
(i.e., parts of the same dataset) and organize them into
one dataset. Datasets are may match only partially
in terms of structure. More details on data can be found
:doc:`here <../basics/data>`. For the time being, let
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
