The configuration file
----------------------

Every server and client uses its own configuration file
that determines how its operations are carried out.
These files are structured in a way that lets you share
the same one across servers and clients to simplify
agreed upon deployment. However, this is not always necessary.
For example, each server owner may customize which
privacy policies are applied on their data.

Configuration is written in
`yaml <https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html>`_.
In general, there are two top-level
bocks: `privacy` to :doc:`declare privacy policies <privacy>` used by servers
to declare a list of privacy policies sequentially applied on map operation outcomes,
and `methods` to
:doc:`declare map-reduce operations <mapreduce>` supported by servers and clients.
A simple configuration file that is shared between a server and client
looks like this:

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.Anonymity
        params:
          k: 2
      - policy: fedmed.privacy.CacheLimit
        params:
          limit: 30
      - policy: fedmed.privacy.ComplexityCap
        params:
          cap: 3

    methods:
      __mul__: fedmed.ops.binary.mul
      __pow__: fedmed.ops.binary.pow
      __add__: fedmed.ops.binary.add
      sum:
        map: fedmed.ops.private.sum
        reduce: fedmed.ops.public.sum
      len:
        map: fedmed.ops.private.num
        reduce: fedmed.ops.public.sum

.. tip:: A configuration file with common options to adjust can be
    found in the library's examples `here <https://github.com/maniospas/FedMed/blob/main/example/config.yaml>`_ .