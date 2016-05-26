# Data Files for *A Systems Approach to Reverse Engineer Lifespan Extension by Dietary Restriction*

**PMID**: [26959186](http://www.ncbi.nlm.nih.gov/pubmed/26959186)
**DOI**: [10.1016/j.cmet.2016.02.002](http://doi.org/10.1016/j.cmet.2016.02.002)
**GEO**: [GSE77110](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE77110)

---

## Directory Contents

### Raw Data

- `GSE77110_series_matrix.txt`: The original raw gene expression data as downloaded from the Gene Ontology Omnibus.
    - Retrieved on 2016-05-06 from [GEO](ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE77nnn/GSE77110/matrix/GSE77110_series_matrix.txt.gz)

### Processing Scripts

- `prepare_data.ipynb`: Parses and restructures the raw GSE77110 data for analysis.

### Processed Data

- `sample_metadata.tsv`: Metadata file containing the treatment conditions for each sample.

- `annot_GSE77110.tsv`: A reshaped and annotated version of the raw data for GSE77110.
