from fedmed.stats.base import mean, std


def pearson(d1, d2):
    return min(1, mean(d1*d2)-mean(d1)*mean(d2))/(std(d1)*std(d2))
