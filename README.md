# GTF2CSV

Transform GTF/GFF2 to CSV for your convenience, e.g. insert it into a database
or load it into pandas dataframe for slicing and dicing.


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
usage: gtf2csv.py [-h] -f GTF [-o OUTPUT] [-t NUM_CPUS]

Convert GTF file to plain csv

optional arguments:
  -h, --help            show this help message and exit
  -f GTF, --gtf GTF     the GTF file to convert
  -o OUTPUT, --output OUTPUT
                        the output filename, if not specified, would just set
                        it to be the same as the input but with extension
                        replaced (gtf => csv)
  -t NUM_CPUS, --num-cpus NUM_CPUS
                        number of cpus for parallel processing, default to all
                        cpus available
```


### Converted files for download 

See converted files in the [data](./data) directory

Example:

Here are the first few lines of converted `Homo_sapiens.GRCh38.92.csv.gz`:

| seqname | source | feature    | start | end   | score | strand | frame | CCDS | basic | ccds_id | cds_end_NF | cds_start_NF | exon_id         | exon_number | exon_version | gene_biotype                       | gene_id         | gene_name | gene_source | gene_version | mRNA_end_NF | mRNA_start_NF | protein_id | protein_version | seleno | transcript_biotype                 | transcript_id   | transcript_name | transcript_source | transcript_support_level | transcript_version |
|---------|--------|------------|-------|-------|-------|--------|-------|------|-------|---------|------------|--------------|-----------------|-------------|--------------|------------------------------------|-----------------|-----------|-------------|--------------|-------------|---------------|------------|-----------------|--------|------------------------------------|-----------------|-----------------|-------------------|--------------------------|--------------------|
| 1       | havana | gene       | 11869 | 14409 | .     | +      | .     |      |       |         |            |              |                 |             |              | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        |                                    |                 |                 |                   |                          |                    |
| 1       | havana | transcript | 11869 | 14409 | .     | +      | .     |      | 1.0   |         |            |              |                 |             |              | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | processed_transcript               | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 1       | havana | exon       | 11869 | 12227 | .     | +      | .     |      | 1.0   |         |            |              | ENSE00002234944 | 1           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | processed_transcript               | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 1       | havana | exon       | 12613 | 12721 | .     | +      | .     |      | 1.0   |         |            |              | ENSE00003582793 | 2           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | processed_transcript               | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 1       | havana | exon       | 13221 | 14409 | .     | +      | .     |      | 1.0   |         |            |              | ENSE00002312635 | 3           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | processed_transcript               | ENST00000456328 | DDX11L1-202     | havana            | 1                        | 2                  |
| 1       | havana | transcript | 12010 | 13670 | .     | +      | .     |      | 1.0   |         |            |              |                 |             |              | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | transcribed_unprocessed_pseudogene | ENST00000450305 | DDX11L1-201     | havana            | NA                       | 2                  |
| 1       | havana | exon       | 12010 | 12057 | .     | +      | .     |      | 1.0   |         |            |              | ENSE00001948541 | 1           | 1            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | transcribed_unprocessed_pseudogene | ENST00000450305 | DDX11L1-201     | havana            | NA                       | 2                  |
| 1       | havana | exon       | 12179 | 12227 | .     | +      | .     |      | 1.0   |         |            |              | ENSE00001671638 | 2           | 2            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | transcribed_unprocessed_pseudogene | ENST00000450305 | DDX11L1-201     | havana            | NA                       | 2                  |
| 1       | havana | exon       | 12613 | 12697 | .     | +      | .     |      | 1.0   |         |            |              | ENSE00001758273 | 3           | 2            | transcribed_unprocessed_pseudogene | ENSG00000223972 | DDX11L1   | havana      | 5            |             |               |            |                 |        | transcribed_unprocessed_pseudogene | ENST00000450305 | DDX11L1-201     | havana            | NA                       | 2                  |


### Transformation strategy

The parsing of GTF is based on GTF/GFF2 format specified at
http://uswest.ensembl.org/info/website/upload/gff.html.

The key transformation steps:

1. ignore all lines starting with `#`.
2. convert all columns but the attribute column to csv.
3. Deal with attribute column.

The first step is straightforward, so is the second step as GTF is tab-separated
fairly close to a csv file except the attribute column.

The attribute column contain a list of tag-value pairs, so I decided to convert
each tag into its own column. Some atrribute tag could appear multiple times per
row (e.g. tag, ont)

```
... exon_id "ENSE00001637883"; tag "cds_end_NF"; tag "mRNA_end_NF";
```

They would be converted to binary (1/0) columns with the tag name prefixing the
column name. E.g. the tag values from the above example would be stored in two
columns, respectively:

1. `tag_cds_end_NF`
1. `tag_mRNA_end_NF`


### Other resources

For a complete list of tags: https://www.gencodegenes.org/gencode_tags.html
