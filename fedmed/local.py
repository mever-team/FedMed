from fedmed.serialization import deserialize
import yaml
import importlib
import sys


class Local:
    def __init__(self, data, config="config.yaml"):
        self.data = data
        if isinstance(config, str):
            with open(config, 'r') as file:
                self.config = yaml.safe_load(file)
        else:
            self.config = config

    def __getitem__(self, item):
        return Local(self.data[item], self.config)

    def __mul__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data*data, self.config)

    def __rmul__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data*data, self.config)

    def __add__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data+data, self.config)

    def __radd__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data+data, self.config)

    def __sub__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data-data, self.config)

    def __rsub__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(data-self.data, self.config)

    def __pow__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data**data, self.config)

    def __rpow__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(data**self.data, self.config)

    def __eq__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data == data, self.config)

    def __ne__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data != data, self.config)

    def __lt__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data < data, self.config)

    def __le__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data <= data, self.config)

    def __gt__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data > data, self.config)

    def __ge__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(self.data >= data, self.config)

    def __abs__(self):
        return Local(abs(self.data), self.config)

    def run(self, request):
        method, kwargs = deserialize(request)
        if method not in self.config["methods"]:
            return f"Method {method} not supported"
        method = self.config["methods"][method]["map"]
        package, method = method.split(".")
        importlib.__import__(package)
        method = getattr(sys.modules[package], method)
        return str(method(self.data, **kwargs))
