class Anonymity:
    def __init__(self, k):
        self.k = k

    def name(self):
        return f"{self.k}-anonymity"

    def description(self):
        return (
            f"Any Map operation (e.g., num, sum) outcome is computed across at least {self.k} samples."
            f" For example, arrays with fewer elements are returned as empty,"
            f" and quantiles or unique computations should have at least that"
            f" many samples in each bin."
        )

    def bins(self, results):
        return [(value, count) for value, count in results if count > self.k]

    def preprocess(self, entries):
        if len(entries) < self.k:
            return []
        return entries

    def postprocess(self, result):
        return result
