"""
Common operations that obfuscate too few data samples.
"""


def max(entries):
    if len(entries) <= 1:
        return None
    ret = entries[0]
    for val in entries:
        if val > ret:
            ret = val
    return ret


def min(entries):
    if len(entries) <= 1:
        return None
    ret = entries[0]
    for val in entries:
        if val > ret:
            ret = val
    return ret


def sum(entries):
    if len(entries) == 1:
        return 0
    ret = 0
    for val in entries:
        ret += val
    return ret


def sqsum(entries):
    if len(entries) <= 1:
        return 0
    ret = 0
    for val in entries:
        ret += val*val
    return ret


def num(entries):
    if len(entries) <= 1:
        return 0
    return len(entries)