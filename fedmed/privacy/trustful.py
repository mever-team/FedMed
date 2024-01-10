class Trustful:
    def __init__(self):
        pass

    def on(self, fragment):
        return self

    def name(self):
        return "Trustful"

    def description(self):
        return "Does not modify operations if it is the only\n" "applied policy."

    def bins(self, results):
        return results

    def preprocess(self, entries):
        return entries

    def postprocess(self, result):
        return result

    def acknowledge(self, server, fragment):
        pass
