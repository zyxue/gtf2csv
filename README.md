# GTF2CSV

Transform GTF/GFF2 to CSV for your convenience. May do GFF3 later.

The parsing of GTF is based on GTF/GFF2 format specified at
http://uswest.ensembl.org/info/website/upload/gff.html.

The key transformation steps:

1. ignore all lines starting with `#`.
2. convert all columns but the attribute column to csv.
3. Deal with attribute column.

The first step is straightforward, so is the second step as GTF is tab-separated
fairly close to a csv file except the attribute column.

The attribute column contain a list of tag-value pairs, so I decided to convert
each tag into its own column. The only troublesome one is the "tag" tag
(unfortunate name), which could appear multiple times per row, e.g.

```
... gene_biotype "protein_coding"; transcript_name "SAMD11-011"; transcript_source "havana"; exon_id "ENSE00001637883"; tag "cds_end_NF"; tag "mRNA_end_NF";
```

I decided to create a binary (1/0) column for each of its corresponding values,
which include

1. CCDS
1. cds_start_NF
1. cds_end_NF
1. mRNA_start_NF
1. mRNA_end_NF
1. seleno
1. basic (not appearing in GRCh37.75)

* seleno means that it contains a selenocysteine.
* NF means that it could not be confirmed.

For more details about their meanings, please see
https://www.gencodegenes.org/gencode_tags.html.

At least for the two annotations I tested on, GRCh37.75 and GRCh38.92, "tag" is
the only tag that could appear multiple times. In other GTF files, there could
be other tag with multiplicity above 1, you could check them with the
`check_tag_multiplicity.py` script.

# Usage

The only external package needed is [pandas=>0.18.1](http://pandas.pydata.org/),
whose `read_csv` method could infer compression of input file automatically.

```
python gtf2csv.py [prefix.gtf]
```
Output will be saved as `[prefix].csv`.

# Transformed Examples

I have downloaded and transformed two versions of human genome annotations in the
[`examples`](https://github.com/zyxue/gtf2csv/tree/master/examples) directory:

First 10 lines of **`Homo_sapiens.GRCh37.75.csv.gz`**:

| seqname | source                             | feature    | start | end   | score | strand | frame | CCDS | ccds_id | cds_end_NF | cds_start_NF | exon_id         | exon_number | gene_biotype | gene_id         | gene_name | gene_source    | mRNA_end_NF | mRNA_start_NF | protein_id | seleno | transcript_id   | transcript_name | transcript_source | 
|---------|------------------------------------|------------|-------|-------|-------|--------|-------|------|---------|------------|--------------|-----------------|-------------|--------------|-----------------|-----------|----------------|-------------|---------------|------------|--------|-----------------|-----------------|-------------------| 
| 1       | pseudogene                         | gene       | 11869 | 14412 | .     | +      | .     |      |         |            |              |                 |             | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        |                 |                 |                   | 
| 1       | processed_transcript               | transcript | 11869 | 14409 | .     | +      | .     |      |         |            |              |                 |             | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000456328 | DDX11L1-002     | havana            | 
| 1       | processed_transcript               | exon       | 11869 | 12227 | .     | +      | .     |      |         |            |              | ENSE00002234944 | 1           | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000456328 | DDX11L1-002     | havana            | 
| 1       | processed_transcript               | exon       | 12613 | 12721 | .     | +      | .     |      |         |            |              | ENSE00003582793 | 2           | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000456328 | DDX11L1-002     | havana            | 
| 1       | processed_transcript               | exon       | 13221 | 14409 | .     | +      | .     |      |         |            |              | ENSE00002312635 | 3           | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000456328 | DDX11L1-002     | havana            | 
| 1       | transcribed_unprocessed_pseudogene | transcript | 11872 | 14412 | .     | +      | .     |      |         |            |              |                 |             | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000515242 | DDX11L1-201     | ensembl           | 
| 1       | transcribed_unprocessed_pseudogene | exon       | 11872 | 12227 | .     | +      | .     |      |         |            |              | ENSE00002234632 | 1           | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000515242 | DDX11L1-201     | ensembl           | 
| 1       | transcribed_unprocessed_pseudogene | exon       | 12613 | 12721 | .     | +      | .     |      |         |            |              | ENSE00003608237 | 2           | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000515242 | DDX11L1-201     | ensembl           | 
| 1       | transcribed_unprocessed_pseudogene | exon       | 13225 | 14412 | .     | +      | .     |      |         |            |              | ENSE00002306041 | 3           | pseudogene   | ENSG00000223972 | DDX11L1   | ensembl_havana |             |               |            |        | ENST00000515242 | DDX11L1-201     | ensembl           | 


First 10 lines of **`Homo_sapiens.GRCh38.88.csv.gz`** 

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
