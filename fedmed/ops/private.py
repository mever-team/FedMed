"""
Common operations that obfuscate too few data samples.
"""

from collections import Counter
import inspect


def privatize(method):
    args = inspect.getfullargspec(method)[0]
    assert len(args) in [1, 2]
    use_policy = "policy" in args

    def wrapper(entries, policy):
        entries = policy.preprocess(entries)
        output = method(entries, policy) if use_policy else method(entries)
        return policy.postprocess(output)

    return wrapper


@privatize
def unique(entries, policy):
    counts = Counter(entries)
    return [value for value, _ in policy.bins(counts.items())]


@privatize
def max(entries):
    if not entries:
        return None
    ret = entries[0]
    for val in entries:
        if val > ret:
            ret = val
    return ret


@privatize
def min(entries):
    if not entries:
        return None
    ret = entries[0]
    for val in entries:
        if val > ret:
            ret = val
    return ret


@privatize
def sum(entries):
    ret = 0
    for val in entries:
        ret += val
    return ret


@privatize
def num(entries):
    if not entries:
        return 0
    return len(entries)
