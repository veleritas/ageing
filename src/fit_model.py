"""Python wrapper for the R linear model fitter."""

import os
import rpy2.robjects as robj

def fit_model(df, model_type, interaction):
    """Fit a particular linear model to a drift dataframe.

    Params:
        df: a pandas dataframe
        model_type: one of {"linear", "log_linear"} describing whether drift
            increases linearly or log-linearly with time
        interaction: a Boolean indicating whether to check the interaction term
            between time and the drug treatment
    """

    R = robj.r
    fname = os.path.realpath(__file__).replace(".py", ".R")
    R.source(fname)

    res = R.fit_model(df, model_type, interaction)

    anova_pval = res[0][0]
    adj_rsq = res[1][0]

    return (robj.pandas2ri.ri2py(res[2]) # the coefficient dataframe
        .reset_index()
        .rename(columns = {
            "index": "parameter",
            "Estimate": "estimate",
            "Std. Error": "std_error",
            "t value": "t_value",
            "Pr(>|t|)": "p_value"
        })
        .assign(
            adj_rsq = adj_rsq,
            anova_pvalue = anova_pval,
            interaction = interaction,
            model = model_type
        )
    )
