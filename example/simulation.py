import fedmed as fm
import numpy as np

server = fm.Server(config="config.yaml")
server["treatmentA"] = {
    "Gender": ["Man", "Woman", "Woman", "Man", "Man", "Man", "Woman"]*100,
    "Receptive": ["Yes", "Yes", "Yes", "No", "No", "No", "Yes"]*100
}

data = fm.FedData([
    fm.Simulation(server=server, fragment="treatmentA"),
])

from fedmed.stats.base import std, mean
d1 = data["Gender"] == "Man"
d2 = data["Receptive"] == "Yes"
print("Pearson correlation", min(1, mean(d1*d2)-mean(d1)*mean(d2))/(std(d1)*std(d2)))
