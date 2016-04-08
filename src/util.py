"""Miscellaneous helper functions."""

import pandas as pd

def read_file(floc):
    with open(floc, "r") as fin:
        for line in fin:
            yield line.rstrip("\n")

def subset(conditions, data):
    """Subset a dataframe according to a dictionary of conditions."""
    assert isinstance(conditions, dict)
    assert isinstance(data, pd.DataFrame)

    temp = pd.DataFrame(conditions, columns = list(conditions.keys()))
    return pd.merge(temp, data, how = "left", on = list(conditions.keys()))
