"""
Common operations that obfuscate too few data samples.
"""


def reductor(method):
    def wrapped(entries):
        return method([float(val) for val in entries if val != "None"])
    return wrapped


@reductor
def max(entries):
    if len(entries) <= 0:
        return None
    ret = entries[0]
    for val in entries:
        if val > ret:
            ret = val
    return ret


@reductor
def min(entries):
    if len(entries) <= 0:
        return None
    ret = entries[0]
    for val in entries:
        if val > ret:
            ret = val
    return ret


@reductor
def sum(entries):
    ret = 0
    for val in entries:
        ret += val
    return ret
