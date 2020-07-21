# Demos for IGV remote

All demos scripts require a running IGV with proper authorization.


## `run.py`

This is a minimal example showing how this module work. Please make sure you have changed `sample_gspath`, `tumor_bam`, `normal_bam` with bams within your authorization domain.


## `batch_igv.py`

This scripts takes a table, `sv-demo.tsv`, which contains SV breakpoints for several TCGA WGS bams. The BAM files are in UUID, rather than as a `gs://`, so we need to use [igv-gdc-buddy](https://github.com/getzlab/igv_gdc_buddy) to convert this UUID to signed URL where IGV can accept.

First, clone [igv_gdc_buddy](https://github.com/getzlab/igv_gdc_buddy) repo and add your credential JSON file as described.
Next, in a separate terminal, run `buddy.py` which performs automatic signed url generation.
Finally, run `batch_igv.py` where it reformats UUID to `http://localhost:5000/<uuid>.bam` that got re-route to signed URL.



