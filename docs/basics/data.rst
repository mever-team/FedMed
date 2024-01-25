Data structures
---------------

Here, we describe how data fragments can be structured
and accessed in a uniform way. They do not need to match
exactly between servers, but only satisfy the ducktyped
calls of clients trying to use them in computations.

The abstract typing of data fragments is they should
be json-like structures with lists of numbers or strings
as their basic primitives. In general, you need to
implement Python's `__getitem__` operator to retrieve
a column of the fragment from its name. For example,
this is already implemented if your fragment is a
Pandas dataframe.

As an example, let us consider a data fragment, called
*treatmentA*, that
contains two columns with enough data samples:
*Gender* of patients, and weather
they were *Receptive* to a treatment.
Some server could represent this as:

.. code-block:: python

    import fedmed as fm
    server = fm.Server(config="config.yaml")
    treatmentA = {
        "Gender": ["Man", "Woman", "Woman", "Man", "Man", "Man", "Woman"]*100,
        "Receptive": ["Yes", "Yes", "Yes", "No", "No", "No", "Yes"]*100
    }
    server["treatmentA"] = treatmentA

We now create a dataset that accesses this fragment
by simulating the server running (for quick experimentation) per:

.. code-block:: python

    data = fm.FedData([
        fm.Simulation(server=server, fragment="treatmentA"),
    ])

As example analysis that may run on this data fragment, use
*FedMed* to compute the pearson correlation between gender
and treatment responsiveness:

.. code-block:: python

    from fedmed.stats.base import std, mean
    d1 = data["Gender"] == "Man"
    d2 = data["Receptive"] == "Yes"
    print("Pearson correlation", min(1, mean(d1*d2)-mean(d1)*mean(d2))/(std(d1)*std(d2)))


