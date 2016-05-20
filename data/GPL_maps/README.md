# Gene Expression Omnibus Platform Information

This directory contains information regarding platforms used by the various GEO experiments.

## Directory Contents

### Raw Data

- `Celegans.na35.annot.csv`: File containing annotations for each probe in the [GPL200](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL200) platform.
    - Retrieved from [Affymetrix](http://www.affymetrix.com/analysis/downloads/na35/ivt/Celegans.na35.annot.csv.zip) on 2016-05-09.

### Processing Scripts

- `parse_GPL200.ipynb`: Parser for extracting relevant probe identifier mappings for GPL200.

### Processed Data

- `GPL200_id_mapping.tsv`: A simplified version of the information contained in `Celegans.na35.annot.csv` containing only probe identifier mappings to other database identifiers.
