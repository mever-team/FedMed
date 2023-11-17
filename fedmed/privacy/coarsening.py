class Coarsening:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def name(self):
        return f"{self.value}-coarsening for {self.type}s"

    def description(self):
        return (
            f"Any Map operation (e.g., num, sum) outcome of type {self.type}"
            f" is coarsened to numerical precision {self.value}. This"
            f" includes quantile calculations. Other data types require"
            f" different versions of this rule."
        )

    def bins(self, results):
        return [(value, self.postprocess(count)) for value, count in results]

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        if self.type == str(type(result)):
            return int(result / self.value) * self.value
        return result
