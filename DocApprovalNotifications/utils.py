import collections
import types


def as_collection(item):
    if isinstance(item, collections.Iterable) and not isinstance(item, types.StringType):
        return item
    else:
        return [item]