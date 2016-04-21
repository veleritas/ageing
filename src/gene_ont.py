"""Load the Gene Ontology."""
import pandas as pd
import re

from collections import defaultdict

from .util import read_file


def extract_go_id(s):
    """Extract the first Gene Ontology ID from a string.

    Assumes that the string contains a GO id.
    """
    res = re.search(r'GO:\d{7}', s)
    assert res is not None, "No GO id found in {}".format(s)
    return res.group()


def parse_go_links(floc):
    """Determine the relationship edges of the Gene Ontology."""

    def extract_edge(s):
        """Extract the edge type and target GO term from a string."""
        assert s.startswith("is_a") or s.startswith("relationship"), "Bad edge string"

        dest = extract_go_id(s)
        if s.startswith("is_a"):
            return ("is_a", dest)

        return (s[s.find(" ") + 1 : s.find("GO:") - 1], dest)

    #---------------------------------------------------------------------------

    file_gen = read_file(floc)

    links = defaultdict(lambda: defaultdict(set))
    for line in file_gen:
        if line == "[Term]":
            go_id = extract_go_id(next(file_gen))

            for sub in file_gen:
                if not sub:
                    break

                if sub.startswith("is_a") or sub.startswith("relationship"):
                    edge, dest = extract_edge(sub)
                    links[go_id][edge].add(dest)

    return links


def load_annotations(floc):
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
