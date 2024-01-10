import fnmatch


class Anonymity:
    def __init__(self, k, **kwargs):
        self.k = k
        self.applied = 0
        self.condition = kwargs.get("filter", ["*"])
        self.reject = kwargs.get("reject", [])

    def on(self, fragment):
        for condition in self.reject:
            if fnmatch.fnmatch(fragment, condition):
                return None
        for condition in self.condition:
            if fnmatch.fnmatch(fragment, condition):
                return self
        return None

    def name(self):
        if '\n'.join(self.condition) == '*':
            cond = ""
        else:
            cond = " on:<br>&emsp;<i>"+"<br>&emsp;".join(self.condition).replace("*", '<span style="color: blue;">&lowast;</span>')+'</i>'
        for reject in self.reject:
            cond += "<br>&emsp;<b style=\"color:red\";>ignore</b>&nbsp;&nbsp;<i>" + reject.replace("*",
                                                                                                   '<span style="color: blue;">&lowast;</span>') + '</i>'
        return f'<span class="badge bg-success text-light" style="width:30px">{self.k}</span> Anonymity'+cond

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
            self.applied += 1
            return []
        return entries

    def postprocess(self, result):
        return result

    def acknowledge(self, server, fragment):
        pass
