"""Functions for creating transcriptional drift plots."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings

from .stats import p_val_matrix

def config_plot(func):
    """Configures parameters for a plot locally.

    This function is used as a decorator for functions which return plots. It
    encapsulates the plot with a local set of parameters so that the plot does
    not affect other plots in the same Jupyter notebook.
    """
    def wrapper(*args, **kwargs):
        with plt.rc_context(rc = kwargs.get("rc")):
            return func(*args, **kwargs)

    return wrapper


@config_plot
def plot_p_val_heatmap(data, group_cols, drift_col, **kwargs):
    """Create a heatmap of Levene's test p-values between all group pairs."""
    p_vals = p_val_matrix(data, group_cols, drift_col)

    fig = sns.heatmap(p_vals, annot = True, square = True, linewidths = 0.5)
    fig.set_title("Levene's p-value for every pairwise group")

    return fig


@config_plot
def plot_drift(kind, data, time_col, drift_col, gene_col, title = None,
    groupby = None, **kwargs):
    """Plot the drift values of a group of genes.

    For line plots, plotting <= 20 genes is recommended in order to keep the
    legend legible.

    For boxplots, if a groupby column is provided, then paired boxplots will be
    plotted.
    """
    assert kind in ["line", "box"], "Incorrect figure type!"
    assert isinstance(data, pd.DataFrame), "No dataframe provided!"
    MAX_GENES = 20

    if kind == "line":
        if data[gene_col].nunique() > MAX_GENES:
            warnings.warn("Plotting >{} genes is not recommended".format(MAX_GENES))

        sub = data.pivot(index = time_col, columns = gene_col, values = drift_col)

        fig = sub.plot(kind = "line")
        fig.legend(loc = "center left", bbox_to_anchor = (1, 0.5))
    else:
        fig = sns.boxplot(
            data = data, x = time_col, y = drift_col, showfliers = False,
            hue = groupby
        )

    fig.set_title(title)
    fig.set_ylabel("Drift value")

    # display number of unique genes plotted on the top right corner
    fig.annotate(
        r'$N = {}$'.format(data[gene_col].nunique()),
        xy = (1, 1), xycoords = "axes fraction", fontsize = 16,
        xytext = (5, -10), textcoords = "offset points",
        ha = "left", va = "top"
    )

    return fig

def plot_drift_split_box(data, time_col, drift_col, groupby):
    """Plot the drift values of a group of genes as a boxplot, split according
    to a factor.
    """
    # change to category to include missing groups
    data.loc[:, time_col] = data.loc[:, time_col].astype("category")
    fig = sns.FacetGrid(data, col = groupby)
    fig = fig.map(sns.boxplot, time_col, drift_col, showfliers = False)
    return fig
