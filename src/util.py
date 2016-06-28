"""Miscellaneous helper functions."""

import json
import operator
import pandas as pd

from functools import reduce


def read_file(floc):
    with open(floc, "r") as fin:
        for line in fin:
            yield line.rstrip("\n")

def load_json(floc):
    with open(floc, "r") as fin:
        return json.load(fin)

def subset(conditions, data):
    """Subset a dataframe according to a dictionary of conditions."""
    assert isinstance(conditions, dict)
    assert isinstance(data, pd.DataFrame)

    temp = pd.DataFrame(conditions, columns = list(conditions.keys()))
    return pd.merge(temp, data, how = "left", on = list(conditions.keys()))

def union(v):
    """Return the union of an iterable of sets.

    If the iterable is empty, returns an empty set().
    """
    return reduce(operator.or_, v, set())
