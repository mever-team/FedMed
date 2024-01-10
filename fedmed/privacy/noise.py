import numpy as np
import fnmatch


class Noise:
    def __init__(self, value, type, **kwargs):
        self.value = value
        self.type = type
        self.applied = 0
        self.condition = kwargs.get("filter", ["*"])
        self.reject = kwargs.get("reject", [])

    def name(self):
        if '\n'.join(self.condition) == '*':
            cond = ""
        else:
            cond = " on:<br>&emsp;<i>"+"<br>&emsp;".join(self.condition).replace("*", '<span style="color: blue;">&lowast;</span>')+'</i>'
        for reject in self.reject:
            cond += "<br>&emsp;<b style=\"color:red\";>ignore</b>&nbsp;&nbsp;<i>"+reject.replace("*", '<span style="color: blue;">&lowast;</span>')+'</i>'
        return f'<span class="badge bg-secondary text-light">{self.value}</span> Variance for {self.type}s' + cond

    def description(self):
        return (
            f"Any Map operation (e.g., num, sum) outcome of type {self.type}"
            f" is distorted though noise of variance {self.value}. This"
            f" includes quantile calculations. Other data types require"
            f" different versions of this rule."
        )

    def on(self, fragment):
        for condition in self.reject:
            if fnmatch.fnmatch(fragment, condition):
                return None
        for condition in self.condition:
            if fnmatch.fnmatch(fragment, condition):
                return self
        return None

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
