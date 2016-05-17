# Data Files for *Suppression of transcriptional drift extends C. elegans lifespan by postponing the onset of mortality*

PMID: [26623667](http://www.ncbi.nlm.nih.gov/pubmed/26623667)
DOI: [10.7554/eLife.08833](http://dx.doi.org/10.7554/eLife.08833)

---

## File Contents

### Original Raw Data

- `Q1_Sunitha_RNAseq_36samples_annotated.raw`: Annotated count per million (CPM) expression values provided by Michael.

- `all_samples_cpm.tsv`: Contains the raw RNA-seq counts per million for each of 19619 genes. Converted from the Excel file `all-sample-cpm.xlsx`. Called `rnaseq-std.raw` by Tristan.
    * Column names: Batch #, Sample # (12 samples of 3 batches each)
    * See `sample_metadata.tsv` for the treatment conditions of each sample.

### Processing Scripts

- `clean_annotated_data.ipynb`: Processes `Q1_Sunitha_RNAseq_36samples_annotated.raw` and removes genes without relative log fold expression changes. Produces two output files:
    1. `clean_annotated_cpm_values.tsv`: the expression values of each biological replicate are kept separate, resulting in 36 total samples.
    2. `avg_annotated_cpm_values.tsv`: the expression values for each gene are averaged together across biological replicates, resulting in 12 samples.

### Metadata

- `sample_metadata.tsv`: Contains the treatment condition information for each RNA-seq sample.
