"""Functions for working with drift statistics."""

import numpy as np

def calc_drift(df, groupby, value):
    """Calculate the variance (drift) for a column in a dataframe.

    Params:
        df = pandas dataframe containing the data
        groupby = string or list denoting columns to group the dataframe by
        value = name of column containing the values to calculate variance

    Returns:
        a pandas dataframe containing the variance for each group
    """
    return (df
        .groupby(groupby, as_index = False)
        .agg({value: np.var})
        .rename(columns = {value: "drift"})
    )
