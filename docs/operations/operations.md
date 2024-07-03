# Operations

Here are basic operations supported by clients. These need to be
included in configuration of both clients and servers to use.
Use the `methods` field of the default configuration file
:ref:`here <https://github.com/maniospas/FedMed/blob/main/example/config.yaml>`
as reference of how to include operations in your own configuration.

The configuration file linked above has all the base operations
needed to call the dependent methods enclosed in the 
`fedmed.stats.base` module, as well as run builtin operations.
Available computations are described below.

Direct implementations
----------------------

First is a way to obtain specific columns from datasets that do
have columns with the [] notation. 
Numerical operators +,-,*,/,//,**,==,<=,>=,<,>,!= are also
overloaded and request remote computations to be performed 
on servers, but you cannot access their values from the
client. Results are also federated datasets pointing to
new data fragments.

Next are direct numerical operations: _sum_, _len_, _min_, _max_. 
These compute one value for federated data (e.g., a column).<br>

There is also the _set_ operation that returns a set of unique 
elements (privacy policies take care to not expose information
through this either with practices like k-anonymity), and _round_
that rounds data at a desired precision level. For example,
use `round(x, 0.1)` to convert data to a precision of one decimal
point.

Dependent methods
-----------------

All operations up to now just add one operational unit
to the complexity cap privacy policy by making one
request each. We now show more complicated dependent operations
that are implemented by *FedMed*. These could fail to execute
on servers that do not allow the necessary complexity cap:

* `fm.stats.base.mean(data)` computes the average data value.
* `fm.stats.base.var(data, df=0)` computes data variance for given degrees of freedom.
* `fm.stats.base.std(data, df=0)` similarly computes the standard deviation of data.
* `fm.stats.base.pearson(d1, d2)` computes the pearson correlation between two data columns.

Distribution proxies
--------------------

A final category of methods uses a distribution 
reconstruction process that mimics the true
distribution of underlying data by coarsening
and then filling each interval with uniformly
random noise. This requires
a complexity cap of at least 100, which means
that it may be too intrusive in terms of privacy
for server owners to tolerate. However, concepts
like k-anonymity and differential privacy (by adding
noise) may help alleviate information leakage concerns.

* `fm.stats.base.reconstruct(data, bins=50)` creates a synthetic reconstruction of data. For example, can be used to create histograms. The number of bins denotes the distribution's granularity, but beware that the memory privacy policy is a multiple of this. This operation also increases the required complexity cap by 8.
* `fm.stats.base.wilcoxon(d1, d2, bins=50)` performs a non-parametric wilcoxon test between two data columns. The same considerations for bins apply as above. This increases the required complexity cap by 9 (a value of 12 is recommended as a default to facilitate complex operations).

