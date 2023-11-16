import numpy as np
import fedmed as fm


def mean(data: fm.FedData):
    return data.sum() / data.len()


def std(data: fm.FedData):
    n = data.len()
    return ((data ** 2).sum() / n - (data.sum() / n) ** 2) ** 0.5


sources = [
    fm.Local({"dim": np.array([1, 6])}),  # also use some local data
    fm.Remote(ip="http://127.0.0.1:8000", fragment="test1"),  # run server.py first
    fm.Remote(ip="http://127.0.0.1:8000", fragment="test2"),
]
data = fm.FedData(config="config.yaml").register(sources)
print(abs(data["dim"]).sum())
#print(std(data["dim"]))
