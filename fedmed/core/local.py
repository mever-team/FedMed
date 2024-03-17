import yaml
import importlib
import sys
from fedmed.privacy.trustful import Trustful


def _method(method):
    if isinstance(method, dict):
        method = method["map"]
    package, method = method.rsplit(".", 1)
    importlib.__import__(package)
    return getattr(sys.modules[package], method)


class Local:
    def __init__(self, data, config="config.yaml"):
        self.data = data
        if isinstance(config, str):
            with open(config, "r") as file:
                self.config = yaml.safe_load(file)
        else:
            self.config = config
        self.policy = Trustful()

    def __str__(self):
        return f"Local fast data: {self.data}"

    def __getitem__(self, item):
        return Local(self.data[item], self.config)

    def operator(self, name, other):
        data = other.data if isinstance(other, Local) else other
        assert name in self.config["methods"]
        return Local(
            _method(self.config["methods"][name])(self.data, data), self.config
        )

    def __mul__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__mul__"])(self.data, data), self.config
        )

    def __rmul__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__mul__"])(self.data, data), self.config
        )

    def __add__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__add__"])(self.data, data), self.config
        )

    def __radd__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__add__"])(self.data, data), self.config
        )

    def __sub__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__sub__"])(self.data, data), self.config
        )

    def __rsub__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__sub__"])(data, self.data), self.config
        )

    def __pow__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__pow__"])(self.data, data), self.config
        )

    def __rpow__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__pow__"])(data, self.data), self.config
        )

    def __eq__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__eq__"])(self.data, data), self.config
        )

    def __ne__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__ne__"])(self.data, data), self.config
        )

    def __lt__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__lt__"])(self.data, data), self.config
        )

    def __le__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__le__"])(self.data, data), self.config
        )

    def __gt__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__gt__"])(self.data, data), self.config
        )

    def __ge__(self, other):
        data = other.data if isinstance(other, Local) else other
        return Local(
            _method(self.config["methods"]["__ge__"])(self.data, data), self.config
        )

    def __abs__(self):
        return Local(
            _method(self.config["methods"]["__abs__"])(self.data, None), self.config
        )

    def run(self, request):
        method, kwargs = request
        if method not in self.config["methods"]:
            return f"Method {method} not supported"
        method = _method(self.config["methods"][method]["map"])
        return method(self.data, self.policy, **kwargs)
