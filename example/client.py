import fedmed as fm
from fedmed.stats.base import *


sources = [
    fm.Local(
        {"first": [1, 2, 3, 4, 5, 6, 7, 8], "second": [5, 6, 7, 8, 9]}
    ),  # can also use local data
]
data = fm.FedData(config="config.yaml").register(
    [fm.Remote(ip="http://127.0.0.1:8000", fragment="test")]
)
print(fm.stats.test.Student().reject(data["first"], data["second"]))


print(std(data["second"]))


"""
sources = [fm.Remote(ip="http://127.0.0.1:8000", fragment="tsla")]
data = fm.FedData(sources, config="config.yaml")

print((data["Region"] == "OCEANIA").sum())
"""
