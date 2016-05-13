"""Utilities for processing Gene Expression Omnibus files."""

import pandas as pd

from .util import read_file

def parse_series_matrix(file_loc):
    """Parser for GSE series matrix files.

    File format:
        plain text file
        columns are tab separated
        contains N samples
        metadata lines begin with '!'

    File contents:
        series metadata (two columns)
        sample metadata (N+1 columns)
        !series_matrix_table_begin
        header (N+1 columns)
        M rows of N+1 columns containing expression values (M = number of genes)
        !series_matrix_table_end
        EOF

    Args:
        file_loc: location and name of file (absolute or relative)

    Returns:
        series_metadata
        sample_metadata
        expression_matrix
    """
    raw_series = []
    raw_sample = []
    for line in read_file(file_loc):
        if line == "!series_matrix_table_begin":
            break
        elif line.startswith('!'):
            vals = [v.strip('"') for v in line.lstrip('!').split('\t')]

            v = raw_series if len(vals) == 2 else raw_sample
            v.append(vals)

    series_metadata = pd.DataFrame(raw_series, columns = ["var", "value"])
    sample_metadata = pd.DataFrame(raw_sample).T

    expression_matrix = pd.read_csv(file_loc, sep = '\t', comment = '!')

    sample_metadata = (sample_metadata
        .rename(columns = sample_metadata.iloc[0])
        .drop(0)
        .reset_index(drop = True)
    )

    sample_metadata.columns = sample_metadata.columns.str.replace("Sample_", "")

    return (series_metadata, sample_metadata, expression_matrix)
