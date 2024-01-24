Server setup
============

Declare data fragments
----------------------

Data servers host your data for clients to use. Custom map operations
of the map-reduce scheme are specified in the configuration file.
Sometimes, you will have the same configuration for your servers
and the client that uses them. Find a first default configuration
that you can edit
:ref:`here <https://github.com/maniospas/FedMed/blob/main/example/config.yaml>`,
and replace paths to implementations with your own. Also remove any operations you do not want
to support for privacy reasons. More details on configuring the
server can be found :doc:`here <../config/mapreduce>`.

Creating a server requires only the couple lines of code below.
You can add data and either server instances of the `Server`
class or add them to :doc:`simulations <../basics/simulation>`.

.. code-block:: python

    import fedmed as fm
    server = fm.Server(config="config.yaml")

.. warning:: Privacy policies in the configurations
    may make `fedmed.ops.private` operations inexact.

Each server can contain fragments of several datasets.
Load data as pandas dataframes or combinations of lists and dicts,
and set them as named fragments by using the server as
a dictionary, like below.

.. code-block:: python

    data = [1, 2, 3]  # or dict of lists, pandas dataframe, etc
    server["test array part 1"] = data

Run the server
--------------

You can run a server with a flask-supporting WSGI library,
like waitress. This will let clients include it in data operations.
*FedMed* does not provide any authentication capabilities -
set up a reverse proxy server to restrict who can access
your data with authentication.


.. code-block:: python

    from waitress import serve

    if __name__ == "__main__":
        serve(server.app, host="127.0.0.1", port=8000)

.. tip:: You may use flask to test servers, but for security
    always use an WSGI library or tool for production services.

Information panel
-----------------

Once you start a *FedMed* server you will be able
to access its information panel in its host address. This provides
a summary of :doc:`configuration <../config/aboutconfig>`
and usage patterns. For example, it monitors cashed intermediate
operations, and the frequency of usage of privacy policies.
The information panel looks like this:

.. image:: panel.png
  :width: 600
  :alt: Information panel screenshot.

As an example, take a look at privacy usage. This contains
detailed explanations and usage counts:

.. image:: ops.png
  :width: 600
  :alt: Privacy policy usage screenshot.
