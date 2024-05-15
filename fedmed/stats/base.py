from fedmed.core import FedData, RemoteRunnable
from typing import Optional
import scipy
from random import random
import numpy as np


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
    offset = {}
    for element in set(rounded):
        if discrete is not None:
            element = int(element/discrete+0.5)*discrete
        filter = rounded == element
        count = sum(filter)
        if count > 0:
            if discrete is not None:
                key = sum(filter*data) / count  # place histogram on the center
                offset[key] = element-key
            else:
                key = element
            #assert key not in distr
            distr[key] = distr.get(key, 0)+count
    return distr, offset


def hist(data: FedData, bins: Optional[int] = 50, _info=False):
    mx = None if bins is None else max(abs(data))
    mn = None if bins is None else min(abs(data))
    discrete = None if bins is None else (mx-mn) / bins
    if _info:
        return *distribution(data, discrete), discrete
    return distribution(data, discrete)[0]


def reconstruct(d, bins=50):
    distr, offset, width = hist(d, bins, _info=True)
    if width is None:
        ret = [k for k, v in distr.items() for _ in range(v)]
    else:
        width *= 2
        #ret = [k+width*(i/(v-1)-0.5) for k, v in distr.items() for i in range(v) if v>1]
        ret = list()
        for k, v in distr.items():
            if v % 2 == 1:
                ret.append(k)
                v = v-1
            halfv = v//2
            for i in range(halfv):
                wid = width-abs(offset[k])
                ret.append(k+wid-wid*i/halfv)
                ret.append(k-wid+wid*i/halfv)
    return ret


def wilcoxon(d1, d2, bins=50, **kwargs):
    r = reconstruct(d1-d2, bins=bins)
    #from matplotlib import pyplot as plt
    #plt.hist(r)
    #plt.show()
    return scipy.stats.wilcoxon(r, **kwargs)
