# FedMed

A privacy-aware federated computing scheme 
for statistical dataset analysis. Process data
scattered across multiple privacy-preserving
servers.

## Quickstart client

Set up communication channels with remote
data fragments and organize them into one dataset.

```python
import fedmed as fm
sources = [
    fm.Remote(ip="http://127.0.0.1:5000", fragment="test array 1/2"),
    fm.Remote(ip="http://127.0.0.1:5001", fragment="test array 2/2")
]
data = fm.FedData(sources, config="config.yaml")
```

Call simple operations among those described in the 
configuration file `config.yaml` (find a first default
in the `example/` folder).
The same file could be shared between the client and 
servers, but some servers in your deployment
context may not support some of these
capabilities and will fail dependent computations. 
Operations are performed under a map-reduce scheme.
The map is performed in the servers, and the reduce
on the client. Each server 
is left in control of how it performs its namesake
map method. 

```python
mean = data.sum() / data.len()
print('Mean', mean)
```

:lock: Control of map operations allows server owners 
to set their own privacy policies. For example, 
they may share new internal data compared to 
old ones only when enough new samples are gathered
(in the interim, outcomes on older versions of the
dataset will be exposed).

For the above code to run, you need to set up
some devices to run at the respective ip addresses.


##  Set up a server

Data servers host your data for clients to use.
Custom map operations of the map-reduce scheme
are specified in the configuration file. Sometimes,
you will have the same configuration for your servers
and the client that uses them. Otherwise,
find a first default
in the `example/` folder, and replace the paths to
implementations with your own. Also remove any 
operations you do not want to support for privacy
reasons.

```python
import fedmed as fm
server = fm.Server(config="config.yaml")
```

:construction: To ensure privacy,
`fedmed.ops.private` operations are not always exact.

Each server can contain fragments of several datasets.
Load data as pandas dataframes or combinations
of lists and dicts, and set them as fragments
like below.

```python
data = [1, 2, 3]
server["test array 1/2"] = data
```

Finally, run your server with a flask-supporing
WSGI library, like waitress. 
This will let clients include it in data operations.

```python
from waitress import serve

if __name__ == "__main__":
    serve(server.app, host="127.0.0.1", port=8000)
```

:globe_with_meridians: Set up a reverse proxy server to restrict
who can perform operations on your system.
