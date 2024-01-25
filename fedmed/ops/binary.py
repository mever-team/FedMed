def operator(method):
    def wrapper(a, b):
        if isinstance(a, list) and isinstance(b, list):
            return [method(ae, be) for ae, be in zip(a, b)]
        if isinstance(a, list):
            return [method(ae, b) for ae in a]
        if isinstance(b, list):
            return [method(a, be) for be in b]
        return method(a, b)

    return wrapper


@operator
def pow(a, b):
    return a ** b


@operator
def add(a, b):
    return a + b

@operator
def mul(a, b):
    return a * b


@operator
def sub(a, b):
    return a - b


@operator
def eq(a, b):
    return a == b


@operator
def ne(a, b):
    return a != b


@operator
def lt(a, b):
    return a < b


@operator
def le(a, b):
    return a <= b


@operator
def gt(a, b):
    return a > b


@operator
def ge(a, b):
    return a >= b


def abs(a, _):
    return [ae if ae > 0 else -ae for ae in a]
