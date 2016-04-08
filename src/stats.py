"""Statistical functions for analyzing drift."""

import numpy as np
import pandas as pd

from itertools import combinations
from scipy.stats import levene

def p_val_matrix(data, group_cols, drift_col):
    """Calculate the Levene's test p-value for each unique pair of groups.

    Returns a dataframe containing only the lower left triangle.
    """
    drift = {
        key: df[drift_col]
        for key, df in data.groupby(group_cols)
    }

    groups = sorted(list(drift.keys()))
    temp = pd.DataFrame(index = groups, columns = groups, dtype = np.float)

    for i, j in combinations(groups, 2):
        temp.loc[i, j] = levene(drift[i], drift[j], center = "median")[1]

    return temp.T
