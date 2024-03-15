import fnmatch


class Saturation:
    def __init__(self, **kwargs):
        self.min = kwargs.get("min", None)
        self.max = kwargs.get("max", None)
        self.type = kwargs.get("type", None)
        self.applied = 0
        self.condition = kwargs.get("filter", ["*"])
        self.reject = kwargs.get("reject", [])

    def name(self):
        if '\n'.join(self.condition) == '*':
            cond = ""
        else:
            cond = " on:<br>&emsp;<i>"+"<br>&emsp;".join(self.condition).replace("*", '<span style="color: blue;">&lowast;</span>')+'</i>'
        for reject in self.reject:
            cond += "<br>&emsp;<b style=\"color:red\";>ignore</b>&nbsp;&nbsp;<i>" + reject.replace("*",
                                                                                                   '<span style="color: blue;">&lowast;</span>') + '</i>'
        return f'<span class="badge bg-secondary text-light">[{"-&infin;"if self.min is None else self.min}, {"&infin;" if self.max is None else self.max}]</span> Saturation for {"number" if self.type is None else self.type}s' + cond

    def description(self):
        return (
            f"Any Map operation (e.g., num, sum) outcome{' of type '+self.type if self.type is not None else ''}"
            f" whose outcome lies outside the interval [{'-&infin;'if self.min is None else self.min}, {'&infin;' if self.max is None else self.max}]  "
            f" has that value snapped to the interval's edges. This"
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
        return [(self.postprocess(value), self.postprocess(count)) for value, count in results]

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        if self.type is None or self.type == result.__class__.__name__:
            self.applied += 1
            if self.min is not None and result < self.min:
                result = self.min
            if self.max is not None and result > self.max:
                result = self.max
            return result
        return result

    def acknowledge(self, server, fragment):
        pass
