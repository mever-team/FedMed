import fedmed as fm


def mean(data: fm.FedData):
    return data.sum() / data.len()


def std(data: fm.FedData):
    n = data.len()
    return ((data ** 2).sum() / n - (data.sum() / n) ** 2) ** 0.5


sum = fm.RemoteRunnable("sum")
len = fm.RemoteRunnable("len")
max = fm.RemoteRunnable("max")
min = fm.RemoteRunnable("min")

"""

sources = [
    fm.Local({"dim": [1, 6]}),  # also use some local data
    fm.Remote(ip="http://127.0.0.1:8000", fragment="test1"),  # run server.py first
    fm.Remote(ip="http://127.0.0.1:8000", fragment="test2"),
]
data = fm.FedData(config="config.yaml").register(sources)
print(sum(data["dim"] >= 1))
#print(std(data["dim"]))
"""


sources = [fm.Remote(ip="http://127.0.0.1:8000", fragment="tsla")]
data = fm.FedData(sources, config="config.yaml")
print(data["Region"].set())
print((data["Region"] == "OCEANIA").sum())
print(((data["Region"] == "OCEANIA") > 0).sum())
