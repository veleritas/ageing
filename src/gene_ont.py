"""Utilities for processing the Gene Ontology."""
import pandas as pd
import re

from collections import defaultdict

from .util import read_file
from .util import union


def extract_go_id(s):
    """Extract the first Gene Ontology ID from a string.

    Assumes that the string contains a GO id.
    """
    res = re.search(r'GO:\d{7}', s)
    assert res is not None, "No GO id found in {}".format(s)
    return res.group()


def load_annotations(floc):
    """Load a specific Gene Ontology annotation file."""

    # http://geneontology.org/page/go-annotation-file-gaf-format-21
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

    return (pd.read_csv(floc, sep = '\t', comment = '!', names = columns)
        .drop('database', axis = 1)
    )


def parse_go_defn(floc):
    """Read the go.obo file and return a dataframe with four columns:

    go_id: the GO id
    go_name: the name of the GO term
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


def parse_go_links(floc):
    """Extract the edges relating terms in the Gene Ontology.

    The Gene Ontology is a DAG. Each GO term points to the terms which are above
    it on the hierarchy. A single GO term may have multiple parents. Starting at
    each term and following the edges upwards, one will always arrive at the
    three root nodes:
        GO:0003674 molecular_function
        GO:0005575 cellular_component
        GO:0008150 biological_process

    For our purposes we want to know the children of each GO term, so that we
    can determine which gene annotations belong to each term. This function
    returns the direct children of each node as an adjacency list. All edges in
    the DAG are flipped from their original orientation (edges are from parent
    to child).
    """

    def extract_edge(s):
        """Extract the edge type and target GO term from a string."""
        dest = extract_go_id(s)
        if s.startswith("is_a"):
            return ("is_a", dest)

        return (s[s.find(" ") + 1 : s.find("GO:") - 1], dest)

    #---------------------------------------------------------------------------

    file_gen = read_file(floc)

    children = defaultdict(lambda: defaultdict(set))
    for line in file_gen:
        if line == "[Term]":
            go_id = extract_go_id(next(file_gen))

            for sub in file_gen:
                if not sub:
                    break

                if sub.startswith("is_a") or sub.startswith("relationship"):
                    # edge: go_id --- edge_type ---> dest
                    edge, dest = extract_edge(sub)

                    children[dest][edge].add(go_id)

    return children


def group_genes(children, annots, edge_types):
    """Determine the genes associated with each GO term, taking into account the
    GO hierarchy.

    The GO term for each gene annotation is usually as specific as possible.
    This results in many GO terms with no direct gene associations. Since more
    general GO terms encompass more specific terms by virtue of the GO hierarchy,
    the gene associations should also be propagated upwards.

    Given the direct children of each GO term and the genes annotated with
    each GO term, determines the genes related to each GO term using the GO
    hierarchy.

    Args:
        children: a defaultdict of defaultdict of set containing the direct
            children of each GO term
        annots: a defaultdict of set containing the genes annotated with each GO
            term
        edge_types: a list of types of edges to consider
    """
    assert isinstance(annots, defaultdict), "Annotations should be a defaultdict"

    cache = defaultdict(set)

    def combine(node):
        """Combine the nodes of multiple edge types into one set."""
        return union(children[node][edge] for edge in edge_types)

    def dfs(cur):
        cache[cur] = union(
            cache[child] if child in cache else dfs(child)
            for child in combine(cur)
        ) | annots[cur]

        return cache[cur]

    roots = ['GO:0003674', 'GO:0005575', 'GO:0008150']
    for root in roots:
        dfs(root)

    return cache


def filter_go(go_terms, go_groups, dataframe, id_col):
    """Filters a dataframe of genes down to those which are annotated with a
    group of GO terms.

    :param go_terms: an iterable of strings representing the relevant GO terms
    :param go_groups: a dictionary of go_term: set(gene ids) that describe which
        genes are annotated with each GO term
    :param dataframe: the dataframe containing genes we want to subset
    """
    genes = union(go_groups[term] for term in go_terms)
    temp = pd.DataFrame({id_col: list(genes)})
    return pd.merge(temp, dataframe, how = "left", on = id_col)
