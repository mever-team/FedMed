# Operations

Here are basic operations supported by clients. These need to be
included in configuration of both clients and servers to use.
Use the `methods` field of the default configuration file
`here <https://github.com/maniospas/FedMed/blob/main/example/config.yaml>`_ 
as reference of how to include them in your own configuration.

Once you do, you can find methods that attempt to run
them for your data sources from the `fm.stats.base` module
(recall that the configuration is specific to the data source). 
The main provided operations are described bellow.

First are way to obtain specific columns from datasets that do
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

All operations up to now just add one operational unit
to the complexity cap privacy policy by making one
request each. We now show more complicated dependent operations: 

* `fm.stats.base.mean(data)` computes the average data value.
* `fm.stats.base.var(data, df=0)` computes data variance for given degrees of freedom.
* `fm.stats.base.std(data, df=0)` similarly computes the standard deviation of data.
* `fm.stats.base.pearson(d1, d2)` computes the pearson correlation between two data columns.
* `fm.stats.base.reconstruct(data, bins=50)` creates a synthetic reconstruction of data. For example, can be used to create histograms. The number of bins denotes the distribution's granularity, but beware that the memory privacy policy is a multiple of this. This operation also increases the required complexity cap by 8.
* `fm.stats.base.wilcoxon(d1, d2, bins=50)` performs a non-parametric wilcoxon test between two data columns. The same considerations for bins apply as above. This increases the required complexity cap by 9 (a value of 12 is recommended as a default to facilitate complex operations).

