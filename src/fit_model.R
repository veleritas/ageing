# Fit linear and loglinear models of drift for GO term drift analysis

get_formula <- function(model_type, interaction)
{
    # Return a formula object
    # Can set a linear or loglinear model of the day_harvested column
    # Can also decide if we want + or * for checking the interaction with drug
    return (as.formula(paste0(
        "drift ~ ",
        ifelse(model_type == "linear", "day_harvested", "log(day_harvested)"),
        ifelse(interaction, " * ", " + "),
        "drug"
    )))
}

fit_model <- function(drift, model_type, interaction)
{
    # Fit a linear model for a precalculated drift dataframe.
    # Arguments:
    #   drift: a dataframe
    #     must have columns: drift, day_harvested, drug
    #   model_type: a string; one of ["linear", "loglinear"]
    #   interaction: a boolean
    #
    # Returns:
    #   A list of three elements:
    #     1. The ANOVA pvalue of the model with the interaction term
    #     2. The adjusted p value of the linear model
    #     3. The coefficient matrix of the linear model

    formula <- get_formula(model_type, interaction)
    other_formula <- get_formula(model_type, !interaction)

    model <- lm(formula, data = drift)
    interact <- lm(other_formula, data = drift)

    anova_pval <- anova(model, interact)$`Pr(>F)`[2]

    res <- summary(model)
    adj_r <- res$adj.r.squared

    return (list(anova_pval, adj_r, as.data.frame(res$coefficients)))
}
