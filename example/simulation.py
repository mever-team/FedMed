import fedmed as fm
import numpy as np
from random import random

server = fm.Server(config="config.yaml")
server["treatmentA"] = {
    "Gender": ["Man", "Woman", "Woman", "Man", "Man", "Man", "Woman"] * 100,
    "Receptive": [random() for _ in range(700)],
}

data = fm.FedData(
    [
        fm.Simulation(server=server, fragment="treatmentA"),
    ]
)

_sum = sum
from fedmed.stats import base


d1 = data["Gender"] == "Man"
d2 = data["Receptive"]

distr = base.hist(d2)
print(base.hist(data["Gender"], bins=None))
print(sum(element*value for element, value in distr.items()))
print(base.sum(d2))

#from matplotlib import pyplot as plt
#plt.bar(list(distr.keys()), list(distr.values()))
#plt.show()

print("Pearson correlation", base.pearson(d1, d2))
print(base.wilcoxon(d2, d2-1))
