# Data files for *Age-related behaviors have distinct transcriptional profiles in Caenorhabditis elegans*

PMID: [18778409](http://www.ncbi.nlm.nih.gov/pubmed/18778409)
GEO: [GSE12290](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE12290)

---

## Directory Contents

### Raw Data

- `GSE12290_series_matrix.txt`: The original raw GSE12290 data as downloaded from GEO.

- `behavior_phenotype.tsv`: Information regarding the movement phenotype of each sample.
    These data were obtained via email from Dr. Simon Melov and are not available in the paper's supplementary information or in GSE12290.

- `GPL5859.gal`: An annotation file for the probes used in the GPL5859 platform. Downloaded from GEO.

### Processing Scripts

- `prepare_data.ipynb`: This notebook formats the raw data and merges in all relevant metadata. Also does some simple filtering of genes.

### Output Files

- `sample_metadata.tsv`: Relevant sample metadata.

- `GPL5859_id_map.tsv`: Summary of probe identifier mappings to WormBase IDs.

- `filtered_expression.tsv`: Cleaned GSE12290 expression values with relevant metadata in long format.
