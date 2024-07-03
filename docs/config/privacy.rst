Privacy policies
================

Privacy policies are declared within
:doc:`server configuration files <mapreduce>`
to control how much information is exposed to clients.
Keep in mind that the outcomes of vectorized operations
(that is, operations between columns, like additions)
are not exposed at all. Whereas map-reduce
operations already expose only aggregate quantities to
external clients. However, it may still be important
to add more degrees of anonymity to avoid accidental
information leakage, even under the assumption that
clients are well-meaning.
Below we describe commonly available privacy policies,
although you can also write your own.

Data security
-------------

This describes available privacy policies and how to declare them
inside the configuration file. These policies are important to ensure that sensitive information is handled correctly and that the privacy of individuals is maintained.

**k-Anonymity** Ensures that any computations that return non-None
values are computed across at least k data samples.

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.Anonymity
        params:
          k: 3
          filter: ["*"] # optional (this default is to apply on all fragments)
          reject: []    # optional (this default is to reject nothing)

**Noise Addition** Adds random noise to reduce operation *outcomes* to obscure individual values. The amount of noise should depend on differential privacy needs.

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.Noise
        params:
          value: 0.01
          type: float
          filter: ["*"]
          reject: []

**Coarsening** Reduces the precision of numerical values to a specified level. This is especially needed when noise is added.

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.Coarsening
        params:
          value: 0.1
          type: float
          filter: ["*"]
          reject: []

**Saturation** Limits the outcomes of reduce operations to within a specified range.

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.Saturation
        params:
          min: 0
          max: 100
          type: int
          filter: ["*"]
          reject: []


Workload limits
---------------

**Cache Limit** Restricts the number of cached computations to protect server memory.

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.CacheLimit
        params:
          limit: 100
          filter: ["*"]
          reject: []

**Complexity Cap** Limits the number of dependent operations to prevent overly complex computations. Basically, this is one more than the maximum allowed depth of the abstract syntax tree of vectorized operations.

.. code-block:: yaml

    privacy:
      - policy: fedmed.privacy.ComplexityCap
        params:
          cap: 10
          filter: ["*"]
          reject: []

Custom policies
---------------

To implement a new policy, follow the prototype below. This example shows how to create a new privacy policy that can be applied to server operations.

.. code-block:: python

    class PrivacyPolicy:
        def __init__(self, mandatory_arg0, mandatory_arg1, **kwargs):
            ...
            self.applied = 0  # holds how many times the policy is applied
            # kwargs are optional arguments
            self.condition = kwargs.get("filter", ["*"])
            self.reject = kwargs.get("reject", [])

        def name(self):
            return '<span class="badge bg-secondary text-light">value</span> Policy name (this will appear in the server panel)'

        def description(self):
            return 'Your policy description here (this will appear in the server panel)'

        def on(self, fragment):
            # standard fragment matching on when to apply the policy
            for condition in self.reject:
                if fnmatch.fnmatch(fragment, condition):
                    return None
            for condition in self.condition:
                if fnmatch.fnmatch(fragment, condition):
                    return self
            return None

        def bins(self, results):
            # how to apply the policy when bins of numbers are returned
            return [(value, self.postprocess(count)) for value, count in results]

        def preprocess(self, entries):
            return entries

        def postprocess(self, result):
            # how to apply the policy returning the transformed (more anonymous outcome)
            # this is an example of a coarsening application
            if "float" == result.__class__.__name__:
                self.applied += 1  # keep track of the times the policy was applied
                return int(result / 0.01) * 0.01
            return result

        def acknowledge(self, server, fragment):
            # Called after the server acknowledges the fragment.
            # Workload cap or similar policies can use this method
            # to remove too complex fragments from the server to
            # prevent their reuse. Implement this with care, as
            # it can be catastrophic for those trying to run
            # operations on your data.
            pass

The above policy can be added to a configuration file per
the following snippet. Do not forget to also share the policy
module as a file or installable package
with anyone that will be using the configuration:

.. code-block:: yaml

    privacy:
      # other policies applied before the PrivacyPolicy
      - policy: module.PrivacyPolicy  # module is where to import PrivacyPolicy from
        params:
          mandatory_arg0: ...
          mandatory_arg1: ...
          optional_arg0: ... # may be omitted (typically, the optional arguments are `filer` and `reject`
      # other policies applied after the PrivacyPolicy

    methods:
      # methods implemented by the server