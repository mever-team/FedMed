import numpy as np


class Noise:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.applied = 0

    def name(self):
        return f'<span class="badge bg-secondary text-light">{self.value}</span> Variance for {self.type}s'

    def description(self):
        return (
            f"Any Map operation (e.g., num, sum) outcome of type {self.type}"
            f" is distorted though noise of variance {self.value}. This"
            f" includes quantile calculations. Other data types require"
            f" different versions of this rule."
        )

    def bins(self, results):
        return [(value, self.postprocess(count)) for value, count in results]

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        if self.type == result.__class__.__name__:
            self.applied += 1
            result = result + np.random.normal(0, self.value)
            if self.type == "int":
                result = int(result)
        return result

    def acknowledge(self, server, fragment):
        pass
