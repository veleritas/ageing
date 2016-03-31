"""Functions for creating transcriptional drift plots.
"""

import pandas as pd
import seaborn as sns

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

def plot_drift_box(data, time_col, drift_col, gene_col,
    groupby = None, split = False):
    """Plot the drift values of a group of genes as a boxplot.

    Different choices:
    1. Single figure with one group
    2. Paired boxplots across one figure
    3. Paired boxplots with separate subfigures
    """
    if groupby is not None and split:
        fig = sns.FacetGrid(data, col = groupby)
        fig = fig.map(sns.boxplot, time_col, drift_col, showfliers = False)
    else:
        fig = sns.boxplot(
            data = data, x = time_col, y = drift_col, showfliers = False,
            hue = groupby
        )

    return fig
