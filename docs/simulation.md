# Local Data and Simulation

FedMed offers two data sources that can incorporate data
from the client machine itself: a) a production-ready Local data
source, which creates minimal overhead, and b) a scalable Simulation
data source, which wraps calls to a server without needing to start
a Flask service. The last option offers a fully scalable simulation,
for example to demonstrate proof-of-concept of privacy policies or
new operations in one machine.

## Local data

You may add local data as fragments in your data sources, 
for example to run a client within one of your servers
with exact information. You can mix local and remote sources 
together with no issue.

```python
import fedmed as fm
sources = [
    fm.Local([1, 2, 3, 4, 5, 6, 7, 8]),
    fm.Local([5, 6, 7, 8, 9]),
]

data = fm.FedData(sources, config="config.yaml")
```

:warning: Local data sources do *not* apply any privacy
policies and therefore perform exact computations.
To simulate that outcome of running servers see below.



## Simulation

To create a simulation of a would-be scenario without
the cost of running multiple services, you can use 
a `Simulation` data source. This requires fully setting
up a server with its own configuration, like usual:

```python
import fedmed as fm
server = fm.Server(config="config.yaml")
data = [1, 2, 3]  # or dict of lists, pandas dataframe, etc
server["test array part 1"] = data
```

To add this as a simulated data source do this:
```python
import fedmed as fm
sources = [
    fm.Simulation(server),
]

data = fm.FedData(sources, config="config.yaml")
```

:bulb: You may simulate multiple servers, each with a different privacy policy.

