import yaml
import sys
import importlib


def serialize(request):
    return request
    #method, kwargs = request
    #return "method:"+str(method)+"\nrequest:"+str(kwargs)

def deserialize(request):
    return request
    #return yaml.safe_load(request)


class VirtualDevice:
    def __init__(self, data, config="config.yaml"):
        self.data = data
        if isinstance(config, str):
            with open(config, 'r') as file:
                #self.md5_hash = hashlib.md5(file.read().encode()).hexdigest()
                self.config = yaml.safe_load(file)
        else:
            self.config = config

    def version(self) -> str:
        return self.md5_hash

    def __getitem__(self, item):
        return VirtualDevice(self.data[item], self.config)

    def run(self, request):
        method, kwargs = deserialize(request)
        if method not in self.config["methods"]:
            return f"Method {method} not supported"
        method = self.config["methods"][method]["map"]
        package, method = method.split(".")
        importlib.__import__(package)
        method = getattr(sys.modules[package], method)
        return str(method(self.data, **kwargs))


class FedData:
    def __init__(self, devices=None, config="config.yaml"):
        if isinstance(config, str):
            with open(config, 'r') as file:
                #self.md5_hash = hashlib.md5(file.read().encode()).hexdigest()
                self.config = yaml.safe_load(file)
        else:
            self.config = config
        self.devices = list()
        if devices is not None:
            self.register(devices)

    def __getitem__(self, item):
        return FedData([device[item] for device in self.devices], self.config)

    def register(self, devices):
        self.devices.extend(devices)
        return self

    def run(self, request):
        if isinstance(request, str):
            request = (request, {})
        method, kwargs = request
        method = self.config["methods"][method]["reduce"]
        package, method = method.split(".")
        importlib.__import__(package)
        method = getattr(sys.modules[package], method)
        request = serialize(request)
        results = [device.run(request) for device in self.devices]
        return method(results)

    def __getattr__(self, item):
        if item in ["run", "devices", "config"]:
            return object.__getattribute__(self, item)

        def method(**kwargs):
            return self.run((item, kwargs))
        return method


def mean(data: FedData):
    return data.sum() / data.len()


def std(data: FedData):
    n = data.len()
    return (data.sqsum()/n-(data.sum()/n)**2)**0.5


devices = [
            VirtualDevice([[1]]),
            VirtualDevice([[2, 3]]),
            VirtualDevice([[1, 2, 3]]),
          ]
pooler = FedData().register(devices)
print(mean(pooler[0]))
