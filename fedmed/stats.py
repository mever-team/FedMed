from fedmed.core import FedData


def mean(data: FedData):
    return data.sum() / data.len()


def std(data: FedData):
    n = data.len()
    return ((data ** 2).sum() / n - (data.sum() / n) ** 2) ** 0.5


def ttest(x1: FedData, x2: FedData):
    mean1 = mean(x1)
    mean2 = mean(x2)
    std1 = std(x1)
    std2 = std(x2)
    n1 = x1.len()
    n2 = x2.len()
    return (mean1 - mean2) / (std1 ** 2 / n1 + std2 ** 2 / n2) ** 0.5
