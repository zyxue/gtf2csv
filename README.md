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
pip install git+https://github.com/zyxue/gtf2csv.git#egg=gtf2csv

gtf2csv --gtf [gtf file]

```

```
gtf2csv -h
usage: gtf2csv [-h] -f GTF [-c CARDINALITY_CUTOFF] [-o OUTPUT] [-m {csv,pkl}]
               [-t NUM_CPUS]

Convert GTF file to plain csv

optional arguments:
  -h, --help            show this help message and exit
  -f GTF, --gtf GTF     the GTF file to convert
  -c CARDINALITY_CUTOFF, --cardinality-cutoff CARDINALITY_CUTOFF
                        for a tag that may appear multiple times in the
                        attribute column (so-called multiplicity tag in this
                        program), if its cardinality, i.e. the number of
                        possibles values across all row, is lower than this
                        cutoff, then it's a low-caridnaltiy tag, and each of
                        its possible value would be transformed into a
                        separate binary column. Otherwise, it is a high-
                        cardinality tag and all of its values in one row would
                        be simply concatenated to avoid making too many
                        columns
  -o OUTPUT, --output OUTPUT
                        the output filename, if not specified, would just set
                        it to be the same as the input but with extension
                        replaced (gtf => csv)
  -m {csv,pkl}, --output-format {csv,pkl}
                        pkl means python pickle format, which would results in
                        much faster IO (recommended)
  -t NUM_CPUS, --num-cpus NUM_CPUS
                        number of cpus for parallel processing, default to 1
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

### Conversion strategy

The parsing of GTF is based on GTF/GFF2 format specified at
http://uswest.ensembl.org/info/website/upload/gff.html.

**The key transformation steps**:

1. ignore all lines starting with `#`.
2. convert all columns but the attribute column to csv.
3. Deal with attribute column.

The first two steps are straightforward. Note that GTF is tab-separated, so it
is very similar to a csv file.

The attribute column is a bit more tricky to deal with. Each row of the
attribute column contains a list of tag-value pairs. In principle, every tag
could form its own column. However, some tags could appear multiple times within
one row. A few observed such tags include:

* `tag` tag as in [Ensembl human gtf files](ftp://ftp.ensembl.org/pub/release-93/gtf/homo_sapiens/)
* `ont` tag as in [GENCODE human gtf files](https://www.gencodegenes.org/releases/current.html)
* `ccds_id` as in [Ensembl for Mus_musculus related gtf files](ftp://ftp.ensembl.org/pub/release-93/gtf/mus_musculus_129s1svimj/)

I named these tags are called multiplicity tags, and they are further classified
into two types depending on the number of possible unique values they have. For
those with a low number of possible values, thus low cardinality, each of their
possible values would be transformed into its own binary column under the name
([tag]:[value]). For example, for the follow `tag` tags,

```
... exon_id "ENSE00001637883"; tag "cds_end_NF"; tag "mRNA_end_NF";
```

It would converted into values in two binary (1/0) columns with column names
`tag:cds_end_NF` and `tag:mRNA_end_NF`. 

For multiplicity tags with a high-cardinality (e.g. `ccds_id` with a cardinality
over 20k), converting each value into its own column would result into to many
columns and consume to much memory, thus the possible values would simply be
concatenated. For example, the following entry

```
... ccds_id "CCDS14805"; ccds_id "CCDS78538"; ccds_id "CCDS78539"; ...
```

would become `CCDS14805,CCDS78538,CCDS78539` under the `ccds_id` column.

The cutoff between high-cardinality and low-cardinality tags could be specified
via `-c/--cardinality-cutoff` parameter.


### Other resources

For a complete list of tags: https://www.gencodegenes.org/gencode_tags.html
