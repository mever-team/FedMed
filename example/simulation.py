import fedmed as fm
import numpy as np

server = fm.Server(config="config.yaml")
server["treatmentA"] = {
    "Gender": ["Man", "Woman", "Woman", "Man", "Man", "Man", "Woman"]*100,
    "Receptive": [1, 1, 1, 0, 0, 0, 1]*100
}

data = fm.FedData([
    fm.Simulation(server=server, fragment="treatmentA"),
])

from fedmed.stats.base import pearson
d1 = data["Gender"] == "Man"
d2 = data["Receptive"]
print("Pearson correlation", pearson(d1, d2))
