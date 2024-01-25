Introduction
============

*FedMed* provides a server-client computational model in which data are hosted in servers and clients
are granted permission to perform statistical analysis without looking at them.
We adopt the following terminology in this federated environment:

| **Data fragment** - A piece of a broader dataset that is gathered in one place and admits certain operations. The combined dataset may be fragmented, for example if it hosts personal medical information obtained from different institutions.
| **Server** - Contains non-exposed data fragments and may be hosted by medical institutions. Multiple servers may host parts of the same combined dataset. Learn how to set up a server :doc:`here <../basics/server>`.
| **Client** - Runs statistical tests on combined datasets of data fragments. Is run by a data scientist with server access permissions. Learn how to run client code :doc:`here <../basics/client>`.

Install the library in your environment with:

.. code-block::
    pip install --upgrade yamlres

Context
-------

Clients are considered broadly non-malicious, but server owners can also take steps to ensure
a necessary degree of data privacy. By design, clients can only view aggregate values,
i.e., no personal information. Computations to obtain those values run entirely within each server
on its local data fragments, and clients combine computation outcomes across multiple servers
(akin to a map-reduce scheme).

Each client and server has its own configuration (declared in a `.yaml` file)
that determines which
:doc:`operations <../operations/operations>`
are supported. Operations can be extended
with new ones or replaced with custom implementations. Server configuration includes
:doc:`privacy policies <../config/privacy>` that are set by their owners and
further control information aggregation (e.g., by omitting certain results or
adding noise) to not inadvertently expose individual
values (e.g., the values of one individual).
Given appropriate permissions and support for respective operations,
*FedMed* provides interfaces to perform :doc:`statistical analysis <../operations/tests>`
across the combined private non-disclosed data fragments residing in servers.

Usage
-----

*FedMed* can run in production or simulate proof-of-concepts.
Client and server code linked before refers to production usage.
Learn how to simulate servers with local data
:doc:`statistical analysis <../basics/simulation>`.
