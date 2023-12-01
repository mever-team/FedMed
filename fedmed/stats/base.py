from fedmed.core import FedData, RemoteRunnable


sum = RemoteRunnable("sum")
len = RemoteRunnable("len")
max = RemoteRunnable("max")
min = RemoteRunnable("min")


def mean(data: FedData):
    return sum(data) / len(data)


def var(data: FedData, df: int = 0):
    # df=1 for sample variance
    n = len(data)
    return sum(data ** 2) / (n-df) - sum(data) ** 2 / n / (n-df)


def std(data: FedData, df: int = 0):
    return var(data, df)**0.5
