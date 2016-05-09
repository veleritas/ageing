# Data Files for *A Systems Approach to Reverse Engineer Lifespan Extension by Dietary Restriction*

PMID: [26959186](http://www.ncbi.nlm.nih.gov/pubmed/26959186)
DOI: [10.1016/j.cmet.2016.02.002](http://doi.org/10.1016/j.cmet.2016.02.002)
GEO: [GSE77110](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE77110)

---

## File Contents

- `GSE77110_series_matrix.txt`: The original raw gene expression data as downloaded from the Gene Ontology Omnibus.

- `sample_metadata.tsv`: Metadata file containing the treatment conditions for each sample.
    - Information is parsed from `GSE77110_series_matrix.txt` by `parse_metadata.ipynb`.

- `Celegans.na35.annot.csv`: File containing annotations for each probe used in GSE77110 (the [GPL200](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL200) platform).
    - Retrieved from [Affymetrix](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL200) on 2016-05-09.

- `GPL200_id_mapping.tsv`: A parsed version of the information contained in `Celegans.na35.annot.csv`. Maps probe ids to identifiers in other databases.
    - Created by `parse_affy.ipynb`.

- `annot_GSE77110.tsv`: A reshaped and annotated version of the raw data for GSE77110.
    - Created by `format_data.ipynb`.
