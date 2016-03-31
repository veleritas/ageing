"""Functions for creating transcriptional drift plots.
"""

import pandas as pd

def plot_drift_raw(data, time_col, gene_col, drift_col, title = None):
    """Plot the drift values of a group of individual genes.

    Recommend no more than ~20 genes plotted to avoid overloading the legend.
    """
    assert isinstance(data, pd.DataFrame), "No dataframe provided!"

    sub = data.pivot(index = time_col, columns = gene_col, values = drift_col)

    graph = sub.plot(kind = "line", title = title)
    graph.set_ylabel("Drift value")
    graph.legend(loc = "center left", bbox_to_anchor = (1, 0.5))

    return graph
