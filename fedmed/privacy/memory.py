import fnmatch


class CacheLimit:
    def __init__(self, limit):
        self.limit = limit
        self.applied = 0
        self.condition = ["*"]

    def name(self):
        return f'<span class="badge bg-primary text-light" style="width:30px">{self.limit}</span> Cache limit'

    def description(self):
        return f"Stores up to {self.limit} cached computations." \
               f" This protects your server by limiting total memory size."

    def on(self, fragment):
        return self

    def bins(self, results):
        return results

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        return result

    def acknowledge(self, server, fragment):
        if len(server.history) > self.limit:
            self.applied += 1
            name = server.history.pop(0)
            del server.fragments[name]


class ComplexityCap:
    def __init__(self, cap, **kwargs):
        self.cap = cap
        self.applied = 0
        self.condition = kwargs.get("filter", ["*"])
        self.reject = kwargs.get("reject", [])

    def name(self):
        if '\n'.join(self.condition) == '*':
            cond = ""
        else:
            cond = " on:<br>&emsp;<i>"+"<br>&emsp;".join(self.condition).replace("*", '<span style="color: blue;">&lowast;</span>')+'</i>'
        for reject in self.reject:
            cond += "<br>&emsp;<b style=\"color:red\";>ignore</b>&nbsp;&nbsp;<i>" + reject.replace("*", '<span style="color: blue;">&lowast;</span>') + '</i>'
        return f'<span class="badge bg-primary text-light" style="width:30px">{self.cap}</span> Complexity cap' + cond


    def description(self):
        return f"Prevents computations that involve more than this number of dependent operations." \
               f" For example, this at worst allows multiplication of up to {self.cap}" \
               f" data columns; if you have more than these columns then specific combinations" \
               f" can never be explored by clients. A limit of 0 would prevents non-Map operations."

    def on(self, fragment):
        for condition in self.reject:
            if fnmatch.fnmatch(fragment, condition):
                return None
        for condition in self.condition:
            if fnmatch.fnmatch(fragment, condition):
                return self
        return None

    def bins(self, results):
        return results

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        return result

    def acknowledge(self, server, fragment):
        if fragment.count(".") > self.cap:
            self.applied += 1
            server.history.remove(fragment)
            del server.fragments[fragment]
