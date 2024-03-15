from fedmed.stats.base import *
import scipy


class Test:
    def __init__(self, alpha=None, mode="two-tailed"):
        self.mode = mode
        self.alpha = alpha
        assert mode in ["less", "greater", "two-tailed"]

    def t_statistic(self, x1: FedData, x2: FedData) -> (float, float):
        raise AttributeError("Missing t_statistic implementation")

    def reject(self, x1: FedData, x2: FedData):
        t, df = self.t_statistic(x1, x2)
        if self.mode == "two-tailed":
            t = abs(t)
        elif self.mode == "less":
            t = -t
        p = scipy.stats.t.cdf(-t, df) * (1 + int(self.mode == "two-tailed"))
        return 1 - p if self.alpha is None else (1 - p > self.alpha)


class Welch:
    def t_statistic(self, x1: FedData, x2: FedData):
        n1 = len(x1)
        n2 = len(x2)
        mean1 = mean(x1)
        mean2 = mean(x2)
        var1 = var(x1, df=1)
        var2 = var(x2, df=1)
        # compute degrees of freedom
        num = (var1 / n1 + var2 / n2) ** 2
        denom = (var1 / n1) ** 2 / (n1 - 1) + (var2 / n2) ** 2 / (n2 - 1)
        df = num / denom
        # compute t
        t = (mean1 - mean2) / (var1 / n1 + var2 / n2) ** 0.5
        return t, df


class Student(Test):
    def t_statistic(self, x1, x2):
        n1 = len(x1)
        n2 = len(x2)
        mean1 = mean(x1)
        mean2 = mean(x2)
        var1 = var(x1, df=1)
        var2 = var(x2, df=1)
        # compute degrees of freedom
        df = n1 + n2 - 2
        # compute t
        pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df
        t = (mean1 - mean2) / (pooled_var * (1 / n1 + 1 / n2)) ** 0.5
        return t, df
