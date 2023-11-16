import yaml
import sys
import importlib


class FedData:
    def __init__(self, devices=None, config="config.yaml"):
        if isinstance(config, str):
            with open(config, "r") as file:
                self.config = yaml.safe_load(file)
        else:
            self.config = config
        self.devices = list()
        if devices is not None:
            self.register(devices)

    def __getitem__(self, item):
        return FedData([device[item] for device in self.devices], self.config)

    def __mul__(self, other):
        if isinstance(other, FedData):
            return FedData([device * o for device, o in zip(self.devices, other.devices)])
        return FedData([device * other for device in self.devices], self.config)

    def __rmul__(self, other):
        if isinstance(other, FedData):
            return FedData([device * o for device, o in zip(self.devices, other.devices)])
        return FedData([device * other for device in self.devices], self.config)

    def __add__(self, other):
        if isinstance(other, FedData):
            return FedData([device + o for device, o in zip(self.devices, other.devices)])
        return FedData([device + other for device in self.devices], self.config)

    def __radd__(self, other):
        if isinstance(other, FedData):
            return FedData([device + o for device, o in zip(self.devices, other.devices)])
        return FedData([other + device for device in self.devices], self.config)

    def __sub__(self, other):
        if isinstance(other, FedData):
            return FedData([device - o for device, o in zip(self.devices, other.devices)])
        return FedData([device - other for device in self.devices], self.config)

    def __rsub__(self, other):
        if isinstance(other, FedData):
            return FedData([o - device for device, o in zip(self.devices, other.devices)])
        return FedData([other - device for device in self.devices], self.config)

    def __pow__(self, other):
        if isinstance(other, FedData):
            return FedData([device ** o for device, o in zip(self.devices, other.devices)])
        return FedData([device ** other for device in self.devices], self.config)

    def __rpow__(self, other):
        if isinstance(other, FedData):
            return FedData([o ** device for device, o in zip(self.devices, other.devices)])
        return FedData([other ** device for device in self.devices], self.config)

    def __eq__(self, other):
        if isinstance(other, FedData):
            return FedData([device == o for device, o in zip(self.devices, other.devices)])
        return FedData([device == other for device in self.devices], self.config)

    def __ne__(self, other):
        if isinstance(other, FedData):
            return FedData([device != o for device, o in zip(self.devices, other.devices)])
        return FedData([device != other for device in self.devices], self.config)

    def __lt__(self, other):
        if isinstance(other, FedData):
            return FedData([device < o for device, o in zip(self.devices, other.devices)])
        return FedData([device < other for device in self.devices], self.config)

    def __le__(self, other):
        if isinstance(other, FedData):
            return FedData([device <= o for device, o in zip(self.devices, other.devices)])
        return FedData([device <= other for device in self.devices], self.config)

    def __gt__(self, other):
        if isinstance(other, FedData):
            return FedData([device > o for device, o in zip(self.devices, other.devices)])
        return FedData([device > other for device in self.devices], self.config)

    def __ge__(self, other):
        if isinstance(other, FedData):
            return FedData([device >= o for device, o in zip(self.devices, other.devices)])
        return FedData([device >= other for device in self.devices], self.config)

    def __abs__(self):
        return FedData([abs(device) for device in self.devices], self.config)

    def register(self, devices):
        self.devices.extend(devices)
        return self

    def run(self, request):
        if isinstance(request, str):
            request = (request, {})
        method, kwargs = request
        method = self.config["methods"][method]["reduce"]
        package, method = method.rsplit(".", 1)
        importlib.__import__(package)
        method = getattr(sys.modules[package], method)
        results = [device.run(request) for device in self.devices]
        return method(results)

    def __getattr__(self, item):
        if item in ["run", "devices", "config"]:
            return object.__getattribute__(self, item)

        def method(**kwargs):
            return self.run((item, kwargs))

        return method
