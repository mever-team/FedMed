import fedmed as fm
from fedmed.stats.base import *


server = fm.Server(config="config.yaml")
server["test"] = {"first": [1, 2, 3, 4, 5, 6, 7, 8], "second": [5, 6, 7, 8, 9]}

sources = [
    fm.Simulation(server, "test")
]

data = fm.FedData(sources, config="config.yaml")
print(sum(data["first"]**2+1))
