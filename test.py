import numpy as np
import fedmed as fm


def mean(data: fm.FedData):
    return data.sum() / data.len()


def std(data: fm.FedData):
    n = data.len()
    return ((data**2).sum()/n-(data.sum()/n)**2)**0.5


sources = [
            fm.Local([np.array([1]*2), np.array([1])]),
            fm.Local([np.array([2, 3]*2), np.array([2, 3])]),
            fm.Local([np.array([1, 2, 3]*2), np.array([1, 2, 3])]),
          ]
pooler = fm.FedData().register(sources)
print(mean(pooler[0]))
