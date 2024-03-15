from fedmed.core import FedData, RemoteRunnable

_min = min
_max = max
sum = RemoteRunnable("sum")
len = RemoteRunnable("len")
max = RemoteRunnable("max")
min = RemoteRunnable("min")


def mean(data: FedData):
    return sum(data) / len(data)


def var(data: FedData, df: int = 0):
    # df=1 for sample variance
    n = len(data)
    r = sum(data**2) / (n - df) - sum(data) ** 2 / n / (n - df)
    if r < 0:
        r = 0
    return r


def std(data: FedData, df: int = 0):
    return var(data, df) ** 0.5


def pearson(d1: FedData, d2: FedData):
    return _max(-1, _min(1, mean(d1 * d2) - mean(d1) * mean(d2)) / (std(d1) * std(d2)))
