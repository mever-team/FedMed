import fedmed as fm
from fedmed.stats.base import *


server = fm.Server(config="config.yaml")
server["test"] = {"first": [1, 2, 3, 4, 5, 6, 7, 8], "second": [5, 6, 7, 8, 9]}

communication = fm.SimulatedCommunication(tracker=True)
sources = [
    fm.Simulation(server=server, fragment="test", communication=communication)
]

data = fm.FedData(sources, config="config.yaml")
print(sum(data["first"]**2)/len(data["first"]))
#print(fm.stats.test.Student().reject(data["first"], 1-data["first"]))

import numpy as np
print("Total sent bytes", np.array(communication.sent).sum())
print("Total received bytes", np.array(communication.received).sum())
