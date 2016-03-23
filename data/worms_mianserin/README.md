# Data Files for *Suppression of transcriptional drift extends C. elegans lifespan by postponing the onset of mortality*

PMID: [26623667](http://www.ncbi.nlm.nih.gov/pubmed/26623667)
DOI: [10.7554/eLife.08833](http://dx.doi.org/10.7554/eLife.08833)

---

## File Contents
* `sample_metadata.tsv`: Contains the treatment condition information for each RNA-seq sample.

* `all_samples_cpm.tsv`: Contains the raw RNA-seq counts per million for each of 19619 genes. Converted from the Excel file `all-sample-cpm.xlsx`. Called `rnaseq-std.raw` by Tristan.
    * Column names: Batch #, Sample # (12 samples of 3 batches each)
    * See `sample_metadata.tsv` for the treatment conditions of each sample.

* `annotated_cpm_values.tsv`: Contains annotated RNA-seq count per million (CPM) values for all samples.
    * Called `rnaseq-anno.raw` by Tristan.
    * This file is generated from `Q1_Sunitha_RNAseq_36samples_annotated.raw` by `clean_annotated_data.ipynb`.
