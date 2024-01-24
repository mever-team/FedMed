# FedMed

A privacy-aware federated computing scheme 
to let non-trusted clients
perform statistical analysis. Process data
scattered across multiple servers, each with
its own privacy policy. Merge these remote data 
and local (or simulated) sources.

**Author:** Emmanouil (Manios) Krasanakis<br>
**Contact:** maniospas@hotmail.com<br>
**License:** Apache 2<br>

<details>
<summary><b>Quickstart data server</b></summary>

Install FedMed with:

```
pip install fedmed
```


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

:construction: Privacy policies may make
`fedmed.ops.private` operations inexact.

Each server can contain fragments of several datasets.
Load data as pandas dataframes or combinations
of lists and dicts, and set them as fragments
like below.

```python
data = [1, 2, 3]  # or dict of lists, pandas dataframe, etc
server["test array part 1"] = data
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

---

</details>

<details>
<summary><b>Example client program</b></summary>

Install FedMed with:

```
pip install fedmed
```

Set up communication channels with remote
data fragments (i.e., parts of the same dataset)
and organize them into one dataset. Datasets 
are allowed to only partially match in terms of
structure and operations.

```python
import fedmed as fm
sources = [
    fm.Remote(ip="http://127.0.0.1:8000", fragment="test array part 1"),
    fm.Remote(ip="http://127.0.0.1:8000", fragment="test array part 2")
]
data = fm.FedData(sources, config="config.yaml")
```

Call simple operations among those described in the 
default configuration file `config.yaml` (find a first default
in the `example/` folder) or define new ones.
The same configuration could be shared between the client and 
servers, but this is not mandatory; 
some servers may not support some
capabilities, in which case some computations will fail.

Operations are performed under a map-reduce scheme.
The map is performed in the servers, and the reduce
on the client. Each server is left in control of both
how it performs its namesake map methods, and how it 
distorts outcomes to comply with some privacy policy. 

```python
from fedmed.stats import sum, len
mean = sum(data) / len(data)
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

---

</details>



### Full documentation in https://fedmed.readthedocs.io .