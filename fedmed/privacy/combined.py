import importlib
import sys


class CombinedPolicy:
    def __init__(self, config):
        self.policies = list()
        for specs in config:
            package, method = specs["policy"].rsplit(".", 1)
            importlib.__import__(package)
            init = getattr(sys.modules[package], method)
            self.policies.append(init(**specs["params"]))

    def bins(self, results):
        for policy in self.policies:
            results = policy.bins(results)
        return results

    def preprocess(self, entries):
        for policy in self.policies:
            entries = policy.preprocess(entries)
        return entries

    def postprocess(self, result):
        for policy in self.policies:
            result = policy.postprocess(result)
        return result

    def acknowledge(self, server, fragment):
        for policy in self.policies:
            policy.acknowledge(server, fragment)
