class CacheLimit:
    def __init__(self, limit):
        self.limit = limit
        self.applied = 0

    def name(self):
        return f'<span class="badge bg-primary text-light" style="width:30px">{self.limit}</span> Cache limit'

    def description(self):
        return f"Stores up to {self.limit} cached computations." \
               f" This protects your server by limiting total memory size."

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
    def __init__(self, cap):
        self.cap = cap
        self.applied = 0

    def name(self):
        return f'<span class="badge bg-primary text-light" style="width:30px">{self.cap}</span> Complexity cap'


    def description(self):
        return f"Prevents computations that involve more than this number of dependent operations." \
               f" For example, this at worst allows multiplication of up to {self.cap}" \
               f" data columns; if you have more than these columns then specific combinations" \
               f" can never be explored by clients. A limit of 0 would prevents non-Map operations."

    def bins(self, results):
        return results

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        return result

    def acknowledge(self, server, fragment):
        if fragment.count(":") > self.cap:
            self.applied += 1
            server.history.remove(fragment)
            del server.fragments[fragment]
