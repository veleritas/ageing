# Gene Expression Omnibus Platform Information

This directory contains information regarding platforms used by the various GEO experiments.

## Directory Contents

### Raw Data

- `Celegans.na35.annot.csv`: File containing annotations for each probe in the [GPL200](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL200) platform.
    - Retrieved on 2016-05-09 from [Affymetrix](http://www.affymetrix.com/analysis/downloads/na35/ivt/Celegans.na35.annot.csv.zip)

- `c_elegans.PRJNA13758.WS252.affy_oligo_mapping.txt`: File from WormBase providing annotations for each probe in GPL200.
    - Retrieved on 2016-05-25 from [WormBase](ftp://ftp.wormbase.org/pub/wormbase/releases/current-production-release/species/c_elegans/PRJNA13758/annotation/c_elegans.PRJNA13758.WS252.affy_oligo_mapping.txt.gz)

### Processing Scripts

- `parse_GPL200.ipynb`: Parser for extracting relevant probe identifier mappings for GPL200.

### Processed Data

- `GPL200_wormbase_map.tsv`: File for converting Affymetrix probes in GPL200 to WormBase identifiers.
