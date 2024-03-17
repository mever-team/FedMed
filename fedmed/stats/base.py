from fedmed.core import FedData, RemoteRunnable
from typing import Optional

_min = min
_max = max
_set = set
_sum = sum
sum = RemoteRunnable("sum")
len = RemoteRunnable("len")
max = RemoteRunnable("max")
min = RemoteRunnable("min")
set = RemoteRunnable("set")
round = RemoteRunnable("round")


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


def distribution(data: FedData, discrete: Optional[float]):
    distr = {}
    rounded = data if discrete is None else round(data, discrete)
    for element in set(rounded):
        if discrete is not None:
            element = int(element/discrete+0.5)*discrete
        count = sum(rounded==element)
        if count > 0:
            distr[element] = distr.get(element, 0)+count
    return distr


def hist(data: FedData, bins: Optional[int] = 20):
    discrete = None if bins is None else (max(abs(data)) - min(abs(data))) / bins
    print("decr" , discrete)
    return distribution(data, discrete)


def wilcoxon(d1, d2, bins=20):
    d = abs(d1-d2)
    distr = hist(d, bins)
    print("distr", distr)
    def count_smaller(x, d):
        return _sum(v for k, v in d.items() if k < x)
    d = _sum(count_smaller(k, d)*v for k, v in distr.items())
    return d