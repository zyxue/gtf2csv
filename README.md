# GTF2CSV

Convert GTF/GFF2 to CSV for your convenience, e.g. insert it into a database or
load it into pandas dataframe for slicing and dicing.

### Download 

I have converted some GTF files that are available for download at
https://gitlab.com/zyxue/gtf2csv-csvs.

Example:

Here are the first few lines of converted [Homo_sapiens.GRCh38.93.csv.gz](./download/ensembl):

| index | seqname | source | feature    | start | end   | score | strand | frame | ccds_id | exon_id         | exon_number | exon_version | gene_biotype                       | gene_id         | gene_name | gene_source | gene_version | protein_id | protein_version | tag:CCDS | tag:basic | tag:cds_end_NF | tag:cds_start_NF | tag:mRNA_end_NF | tag:mRNA_start_NF | tag:seleno | transcript_biotype   | transcript_id   | transcript_name | transcript_source | transcript_support_level | transcript_version |
|-------|---------|--------|------------|-------|-------|-------|--------|-------|---------|-----------------|-------------|--------------|------------------------------------|-----------------|-----------|-------------|--------------|------------|-----------------|----------|-----------|----------------|------------------|-----------------|-------------------|------------|----------------------|-----------------|-----------------|-------------------|--------------------------|--------------------|
| 0     | 1       | havana | gene       | 11869 | 14409 | .     | +      | .     |         |                 |             |              | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |            |                 |          |           |                |                  |                 |                   |            |                      |                 |                 |                   |                          |                    |
| 1     | 1       | havana | transcript | 11869 | 14409 | .     | +      | .     |         |                 |             |              | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |            |                 |          | 1         |                |                  |                 |                   |            | processed_transcript | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 2     | 1       | havana | exon       | 11869 | 12227 | .     | +      | .     |         | ENSE00002234944 | 1           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |            |                 |          | 1         |                |                  |                 |                   |            | processed_transcript | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 3     | 1       | havana | exon       | 12613 | 12721 | .     | +      | .     |         | ENSE00003582793 | 2           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |            |                 |          | 1         |                |                  |                 |                   |            | processed_transcript | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 4     | 1       | havana | exon       | 13221 | 14409 | .     | +      | .     |         | ENSE00002312635 | 3           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |            |                 |          | 1         |                |                  |                 |                   |            | processed_transcript | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |

### Install & Usage

require python>=3.6

```
virtualenv venv
. venv/bin/activate
pip install pandas tqdm

python gtf2csv.py --gtf [input-gtf]
```

```
python gtf2csv.py --help
usage: gtf2csv.py [-h] -f GTF [-o OUTPUT] [-m {csv,pkl}] [-t NUM_CPUS]

Convert GTF file to plain csv

optional arguments:
  -h, --help            show this help message and exit
  -f GTF, --gtf GTF     the GTF file to convert
  -o OUTPUT, --output OUTPUT
                        the output filename, if not specified, would just set
                        it to be the same as the input but with extension
                        replaced (gtf => csv)
  -m {csv,pkl}, --output-format {csv,pkl}
                        pkl means python pickle format, which would results in
                        much faster IO (recommended)
  -t NUM_CPUS, --num-cpus NUM_CPUS
                        number of cpus for parallel processing, default to all
                        cpus available
```

### Comparison of GTF versions

I converted most ensemebl gtf releases and compared them from different aspects
([notebook](https://github.com/zyxue/gtf2csv/blob/master/notebooks/Comparison-of-GTF-versions-all-Ensembl-releases.ipynb)).

**Number of protein coding genes**

A gene is considered protein coding if at least one its transcripts is protein
coding. The number has been relatively stable around 20k for a long time.


<img src="https://gitlab.com/zyxue/gtf2csv-csvs/raw/master/figs/num_protein_coding_genes.jpg" alt width="100%">


Different colors indicate major genome update, i.e. GRCh36/hg18 (blue),
GRCh37/hg19 (red), GRCh38/hg38 (yellow).


**Number of protein coding transcripts**

Considering the current number is 80k, so on average a gene has 4 protein coding
transcripts.

<img src="https://gitlab.com/zyxue/gtf2csv-csvs/raw/master/figs/transcripts/protein_coding_transcripts.jpg" alt width="100%">


**Number of lincRNA**

<img src="https://gitlab.com/zyxue/gtf2csv-csvs/raw/master/figs/transcripts/lincRNA_transcripts.jpg" alt width="100%">

As seen, lincRNA hasn't been annotated until around GRCh37.57 (2010-03 based on
https://www.gencodegenes.org/releases/).

For all available transcript types, please see
https://gitlab.com/zyxue/gtf2csv-csvs/tree/master/figs.

**More detailed comparison of a few select versions**

The early version of annotation, Homo_sapiens.GRCh37.75.pkl, has many more genes
and transcripts than later ones, (~14% and ~9.7% increase in numbers for protein
coding gene and transcripts, respectively when compared to
Homo_sapiens.GRCh38.93.pkl. Below are more details. For the generation of the
table of figures, please refere to this
[notebook](./notebooks/Comparison-of-GTF-versions.ipynb).


| index | version                    | num_protein_coding_genes | num_protein_coding_transcripts | num_all_genes | num_all_transcripts |
|-------|----------------------------|--------------------------|--------------------------------|---------------|---------------------|
| 0     | Homo_sapiens.GRCh37.75.pkl | 22810                    | 90274                          | 63677         | 215171              |
| 1     | Homo_sapiens.GRCh37.87.pkl | 20356                    | 81787                          | 57905         | 196502              |
| 2     | Homo_sapiens.GRCh38.92.pkl | 19912                    | 82307                          | 58395         | 203743              |
| 3     | Homo_sapiens.GRCh38.93.pkl | 19912                    | 82307                          | 58395         | 203743              |
| 4     | gencode.v28.annotation.pkl | 19901                    | 82335                          | 58381         | 203836              |

<img src="https://raw.githubusercontent.com/zyxue/gtf2csv/master/gtf-comparison.jpg" alt="" width=600>


### Conversion strategy

The parsing of GTF is based on GTF/GFF2 format specified at
http://uswest.ensembl.org/info/website/upload/gff.html.

**The key transformation steps**:

1. ignore all lines starting with `#`.
2. convert all columns but the attribute column to csv.
3. Deal with attribute column.

The first step is straightforward, so is the second step as GTF is tab-separated
fairly close to a csv file except the attribute column.

The attribute column contain a list of tag-value pairs, so I decided to convert
each tag into its own column under the name ([tag]:[value]). Some atrribute tag
could appear multiple times per row (e.g. tag, ont)

```
... exon_id "ENSE00001637883"; tag "cds_end_NF"; tag "mRNA_end_NF";
```

They would be converted to binary (1/0) columns with the tag name prefixing the
column name. E.g. the tag values from the above example would be stored in two
columns, respectively:

1. `tag:cds_end_NF`
1. `tag:mRNA_end_NF`


### Other resources

For a complete list of tags: https://www.gencodegenes.org/gencode_tags.html
