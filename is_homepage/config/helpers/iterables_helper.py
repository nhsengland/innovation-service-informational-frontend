from functools import reduce


def flatten_tuple(nested_tuple):
    def reducer(acc, val):
        if isinstance(val, tuple):
            return acc + flatten_tuple(val)
        else:
            return acc + (val,)

    return reduce(reducer, nested_tuple, ())
