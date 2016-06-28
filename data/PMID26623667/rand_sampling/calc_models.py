"""
Calculate linear and log-linear drift models for all randomly generated datasets.

Run directly from the terminal. Written as a regular Python script so that
nested tqdm progress bars can be used to monitor progress.

Works best on machines with multiple cores. Runs in approximately 40 minutes on
a 40 core Amazon instance.
"""
import pandas as pd
import sys

from glob import glob
from rpy2.robjects import pandas2ri
from tqdm import tqdm

sys.path.append("../../..")

from src.drift import calc_drift
from src.fit_model import fit_model
from src.util import calc_parallel
from src.util import load_json

#-------------------------------------------------------------------------------

data = (pd
    .read_csv("../clean_annotated_cpm_values.tsv", sep = '\t')
    .query("cohort <= 7 & samples != 62")
    .rename(columns = {"wormbaseid": "wormbase_id", "cohort": "sample"})
    .replace("water", "control")
)

def filter_genes(df, genes):
    """Filter the entire transcriptome down to a group of genes."""

    genes = set(genes)
    return df.query("wormbase_id in @genes")

def model(genes):
    sub = filter_genes(data, genes)

    drift = calc_drift(
        sub, ['sample', 'replicate', 'drug', 'day_harvested'], 'RLFEC'
    )

    res = []
    for model_type in ["linear", "loglinear"]:
        for interaction in [False, True]:
            res.append(fit_model(drift, model_type, interaction))

    return pd.concat(res)

def work(fname):
    """Fit linear and log-linear models to a population of gene sets.

    Return the fitted model parameters as a dataframe.
    """

    gene_sets = load_json(fname)

    uids = list(gene_sets.keys())
    genes = list(gene_sets.values())

    # check that the orders of the values are the same
    assert all(gene_sets[uid] == vals for uid, vals in zip(uids, genes))


    ans = []
    for uid, res in tqdm(zip(uids, calc_parallel(model, genes)), total = len(uids), desc = "Population"):
        ans.append(res.assign(uid = uid))

    return (pd
        .concat(ans)
        .sort_values(["uid", "model", "interaction", "parameter"])
        .reset_index(drop = True)
    )

def main():
    pandas2ri.activate()

    files = glob("genesets/*.json")
    for fname in tqdm(files, desc = "Gene sets"):
        res = work(fname)

        fout = fname.replace("genesets", "models").replace("json", "model")

        res.to_csv(fout, sep = '\t', index = False)

if __name__ == "__main__":
    main()
