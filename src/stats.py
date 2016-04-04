"""Statistical functions for analyzing drift data."""

import numpy as np
import pandas as pd
import seaborn as sns

from itertools import combinations
from scipy.stats import levene

def p_val_matrix(data, group_cols, drift_col):
    """Calculate the Levene's test p-value for each unique pair of groups.

    Only calculates the lower left triangle.
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

def plot_p_val_heatmap(data, group_cols, drift_col):
    p_vals = p_val_matrix(data, group_cols, drift_col)

    fig = sns.heatmap(p_vals, annot = True, square = True, linewidths = 0.5)
    fig.set_title("Levene's p-value for every pairwise group")
    return fig
