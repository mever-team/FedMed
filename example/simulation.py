import fedmed as fm
from random import random, seed

seed(5)
serverA = fm.Server(config="config.yaml")
serverA["fragment"] = {
    "Treatment1": [random() for _ in range(1000)],
    "Treatment2": [random() ** 2 + 0.22 for _ in range(1000)],
}
serverB = fm.Server(config="config.yaml")
serverB["fragment"] = {
    "Treatment1": [random() for _ in range(300)],
    "Treatment2": [random() ** 2 + 0.25 for _ in range(300)],
}

data = fm.FedData(
    [
        fm.Simulation(server=serverA, fragment="fragment"),
        fm.Simulation(server=serverB, fragment="fragment"),
    ]
)

treat1 = data["Treatment1"]
treat2 = data["Treatment2"]

print(fm.stats.base.wilcoxon(treat1, treat2))

distr = fm.stats.base.reconstruct(
    treat1 - treat2
)  # synthetic estimation based on privacy-aware operations
from matplotlib import pyplot as plt

plt.hist(distr)
plt.show()
