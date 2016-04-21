"""Load the Gene Ontology."""
import pandas as pd
from collections import defaultdict

from .util import read_file

def load_go(floc):
    """Read the Gene Ontology annotations for this organism."""
    def num_skip(fname):
        """Count the number of lines to skip at the head of a Gene Ontology file."""
        for i, line in enumerate(read_file(fname)):
            if not line.startswith("!"):
                return i

        raise Exception("File only contained comments!")

    columns = [
        "database",
        "database_id",
        "db_obj_symbol",
        "qualifier",
        "go_id",
        "db_ref",
        "evidence",
        "with_from",
        "aspect",
        "db_obj_name",
        "db_obj_syn",
        "db_obj_type",
        "taxon",
        "date",
        "assigned_by",
        "annot_ext",
        "gene_prod_id"
    ]

    nskip = num_skip(floc)

    data = pd.read_csv(floc, sep = '\t', skiprows = nskip, names = columns)
    return data.drop("database", axis = 1) # redundant column

def parse_go_defn(floc):
    """Read the go.obo file and return a dataframe with four columns:

    id: the GO id
    name: the name of the GO term
    namespace: one of [biological_process, molecular_function, cellular_component]
    obsolete: a boolean
    """
    res = defaultdict(list)

    gen = read_file(floc)
    for line in gen:
        if line == "[Term]":
            obsolete = False
            for sub in gen:
                if not sub:
                    break

                idx = sub.find(":")
                key = sub[: idx]
                if key in ["id", "name", "namespace"]:
                    res[key].append(sub[idx + 2 :])
                elif key == "is_obsolete":
                    obsolete = True

            res["obsolete"].append(obsolete)

    return pd.DataFrame(res).rename(columns = {"id": "go_id", "name": "go_name"})
