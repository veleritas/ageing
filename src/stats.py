"""Statistical functions for analyzing drift."""

from itertools import combinations
from scipy.stats import levene
from scipy.stats.mstats import rankdata

def calc_percentile(values):
    """Calculates the percentile values for a sample of numbers.

    NOTE:
        There are multiple ways to calculate the percentile. The problem lies in
        how to deal with duplicate entries.

        We will use the simplest definition of percentile, which is the rank of
        an entry divided by the total number of entries. When calculating the
        rank, we take the mean ranks of all entries with the same value.

        The calculated percentiles are in [0, 100).
    """
    return (rankdata(values) - 1) / len(values) * 100


def p_val_pairs(data, group_cols, drift_col, get_groups = False):
    """Calculate the Levene's test p-value for each unique pair of groups.

    Also calculates whether the first group has a larger variance than the
    second group. Does not calculate for all pairs!

    Returns:
        res[(groupA, groupB)] = (p-value, var(groupA) > var(groupB))

        and the unique groups in sorted order
    """
    drift = {key: df[drift_col] for key, df in data.groupby(group_cols)}

    groups = sorted(list(drift.keys()))

    p_vals = {
        (i, j): (
            levene(drift[i], drift[j], center = "median")[1],
            drift[i].var() > drift[j].var()
        )
        for i, j in combinations(groups, 2)
    }

    return (p_vals, groups) if get_groups else p_vals
