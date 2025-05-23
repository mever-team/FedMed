import fedmed as fm
from random import random, seed
from matplotlib import pyplot as plt
import numpy as np
seed(5)
dA1 = [random() for _ in range(1000)]
dA2 = [random() ** 2 + 0.22 for _ in range(1000)]
dB1 = [random() for _ in range(1)]
dB2 = [random() ** 2 + 0.25 for _ in range(1)]

serverA = fm.Server(config="config.yaml")
serverA["fragment"] = {
    "Treatment1": dA1,
    "Treatment2": dA2,
}
serverB = fm.Server(config="config.yaml")
serverB["fragment"] = {
    "Treatment1": dB1,
    "Treatment2": dB2,
}


data = fm.FedData(
    [
        fm.Simulation(server=serverA, fragment="fragment"),
        fm.Simulation(server=serverB, fragment="fragment"),
    ]
)
# synthetic estimation based on privacy-aware operations
diff_distribution = fm.stats.base.reconstruct(data["Treatment1"] - data["Treatment2"])
plt.hist(diff_distribution, label="estimated", alpha=0.5)



plt.hist(np.array(dA1+dB1)-np.array(dA2+dB2), label="true", alpha=0.5)
plt.legend()
plt.show()



"""
plt.hist(np.array(dA1+dB1)-np.array(dA2+dB2), label=f"true pvalue {scipy.stats.wilcoxon(dA1+dB1, dA2+dB2).pvalue:.4f}")
plt.hist(distr, label=f"estimated pvalue {fm.stats.base.wilcoxon(treat1, treat2).pvalue:.4f}")
"""