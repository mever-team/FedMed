# FedMed

A privacy-aware federated computing scheme 
for statistical dataset on data found
across multiple servers without data access.

## Quickstart client

*This is still design fiction.*

Set up communication channels with remote
data fragments and organize them into one dataset. 

```python
import fedmed as fm
sources = [
    fm.Remote(ip="localhost:8000", fragment="test array 1/2"),
    fm.Remote(ip="localhost:8001", fragment="test array 2/2")
]
data = fm.FedData(sources, config="config.yaml")
```

Call simple operations among those described in the 
configuration file `config.yaml`. Operations are
performed under a map-reduce scheme. However,
each device is left of control of which map operations
it is allowed to perform.

```python
mean = data.sum() / data.len()
print('Mean', mean)
```

:bulb: Control of operations allows devices to
set their own privacy policies. For example, 
they may share new internal data compared to 
old ones only when enough new samples are gathered
(in the interim, outcomes on older versions of the
dataset will be exposed).

For the above code to run, you need to set up
some devices to run at the respective ip addresses.


## Quickstart server

Data servers host your data for clients to use.
Custom map operations of the map-reduce scheme
are specified in the configuration file (usually,
you will have the same configuration for your servers
and the client that uses them).

```python
import fedmed as fm
server = fm.Server(config="config.yaml")
```

Each server can contain fragments of several datasets.
Load data as pandas dataframes or combinations
of lists and dicts, and register them as fragments
like below. You can register new versions of the
fragment.

```python
data = [1, 2, 3]
server["test array 1/2"] = data
```

Finally, run your server forever to let clients use
it for data sources.

```python
server.run()
```

:bulb: Set up a reverse proxy server to ensure
that not anybody can perform operations on your system.
