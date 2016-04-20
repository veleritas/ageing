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
    """Return a dataframe of the GO term and its name."""
    res = defaultdict(list)

    file_gen = read_file(floc)
    for line in file_gen:
        if line == "[Term]":
            uid = next(file_gen)
            name = next(file_gen)

            assert uid.startswith("id: GO:"), "Bad id for {}".format(uid)
            assert name.startswith("name: "), "Bad name for {}".format(name)

            res["go_id"].append(uid[4:])
            res["go_name"].append(name[6:])

    return pd.DataFrame(res)
