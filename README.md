# GTF2CSV (Bug, cannot handle multiple tags inside one entry)

Converts GTF (aka. GFF2) to CSV for your convenience. May do GFF3 later.

# Usage

Based on GFF format specified at
http://uswest.ensembl.org/info/website/upload/gff.html.

All lines starting with `#` are ignored for simplicity.

It needs [pandas](http://pandas.pydata.org/) to run

```
python gtf2csv.py [prefix.gtf]
```

Output will be saved as `prefix.csv`.

Included are a couple of already converted GTF files. URLS of the GTF files are
listed in `gtf_urls.txt`:

# Development

Test

```
pytest test_gtf2csv.py
```

# Examples

You can go to `examples` directory, download both versions of human genome
annotations, the transform them into csv and compare as below.

Included columns in transformed **`Homo_sapiens.GRCh37.75.csv.gz`** are

```
 1 seqname                      2 source                       3 feature                     
 4 start                        5 end                          6 score                       
 7 strand                       8 frame                        9 ccds_id                     
10 exon_id                     11 exon_number                 12 gene_biotype                
13 gene_id                     14 gene_name                   15 gene_source                 
16 protein_id                  17 tag                         18 transcript_id               
19 transcript_name             20 transcript_source           
```

10 sampled lines:

|         | seqname     | source               | feature | start    | end      | score | strand | frame | ccds_id   | exon_id         | exon_number | gene_biotype   | gene_id         | gene_name    | gene_source    | protein_id      | tag           | transcript_id   | transcript_name  | transcript_source |
|---------|-------------|----------------------|---------|----------|----------|-------|--------|-------|-----------|-----------------|-------------|----------------|-----------------|--------------|----------------|-----------------|---------------|-----------------|------------------|-------------------|
| 929894  | 7           | protein_coding       | exon    | 12423162 | 12423227 | .     | -      | .     | CCDS47544 | ENSE00003532180 | 4.0         | protein_coding | ENSG00000146530 | VWDE         | ensembl_havana | NaN             | CCDS          | ENST00000275358 | VWDE-001         | ensembl_havana    |
| 1483272 | 11          | protein_coding       | exon    | 65629418 | 65629516 | .     | +      | .     | NaN       | ENSE00003502854 | 2.0         | protein_coding | ENSG00000172732 | MUS81        | ensembl_havana | NaN             | mRNA_start_NF | ENST00000530111 | MUS81-014        | havana            |
| 1783038 | 14          | protein_coding       | CDS     | 50459496 | 50459591 | .     | -      | 1     | CCDS41949 | NaN             | 2.0         | protein_coding | ENSG00000214900 | C14orf182    | ensembl_havana | ENSP00000382157 | CCDS          | ENST00000399206 | C14orf182-001    | ensembl_havana    |
| 1786335 | 14          | retained_intron      | exon    | 53118957 | 53119026 | .     | -      | .     | NaN       | ENSE00003687454 | 6.0         | protein_coding | ENSG00000197930 | ERO1L        | ensembl_havana | NaN             | NaN           | ENST00000556769 | ERO1L-007        | havana            |
| 1922708 | 15          | protein_coding       | exon    | 82563944 | 82564435 | .     | +      | .     | NaN       | ENSE00002585154 | 4.0         | protein_coding | ENSG00000188659 | FAM154B      | ensembl_havana | NaN             | NaN           | ENST00000565432 | FAM154B-005      | havana            |
| 1997267 | 16          | protein_coding       | exon    | 29851724 | 29851780 | .     | +      | .     | NaN       | ENSE00002606647 | 4.0         | protein_coding | ENSG00000013364 | MVP          | ensembl_havana | NaN             | mRNA_end_NF   | ENST00000563558 | MVP-018          | havana            |
| 2007111 | 16          | processed_pseudogene | exon    | 33573502 | 33573715 | .     | +      | .     | NaN       | ENSE00002624250 | 1.0         | pseudogene     | ENSG00000260308 | RP11-104C4.4 | havana         | NaN             | NaN           | ENST00000563187 | RP11-104C4.4-001 | havana            |
| 2426837 | 19          | protein_coding       | exon    | 39903225 | 39904052 | .     | +      | .     | CCDS33022 | ENSE00001834377 | 1.0         | protein_coding | ENSG00000090924 | PLEKHG2      | ensembl_havana | NaN             | CCDS          | ENST00000409794 | PLEKHG2-001      | ensembl_havana    |
| 2435042 | 19          | lincRNA              | exon    | 42042076 | 42042145 | .     | +      | .     | NaN       | ENSE00001910792 | 2.0         | lincRNA        | ENSG00000270164 | AC006129.4   | havana         | NaN             | NaN           | ENST00000494375 | AC006129.4-001   | havana            |
| 2788068 | HG747_PATCH | protein_coding       | exon    | 65944197 | 65944422 | .     | +      | .     | NaN       | ENSE00002642203 | 5.0         | protein_coding | ENSG00000262858 | BPTF         | havana         | NaN             | mRNA_start_NF | ENST00000579610 | BPTF-005         | havana            |


Included columns in transformed **`Homo_sapiens.GRCh38.88.csv.gz`** are

```
 1 seqname                      2 source                       3 feature                     
 4 start                        5 end                          6 score                       
 7 strand                       8 frame                        9 ccds_id                     
10 exon_id                     11 exon_number                 12 exon_version                
13 gene_biotype                14 gene_id                     15 gene_name                   
16 gene_source                 17 gene_version                18 havana_gene                 
19 havana_gene_version         20 havana_transcript           21 havana_transcript_version   
22 protein_id                  23 protein_version             24 tag                         
25 transcript_biotype          26 transcript_id               27 transcript_name             
28 transcript_source           29 transcript_support_level    30 transcript_version          
```

10 sampled lines:

|         | seqname | source         | feature         | start     | end       | score | strand | frame | ccds_id   | exon_id         | exon_number | exon_version | gene_biotype   | gene_id         | gene_name    | gene_source    | gene_version | havana_gene        | havana_gene_version | havana_transcript  | havana_transcript_version | protein_id      | protein_version | tag         | transcript_biotype      | transcript_id   | transcript_name  | transcript_source | transcript_support_level | transcript_version |
|---------|---------|----------------|-----------------|-----------|-----------|-------|--------|-------|-----------|-----------------|-------------|--------------|----------------|-----------------|--------------|----------------|--------------|--------------------|---------------------|--------------------|---------------------------|-----------------|-----------------|-------------|-------------------------|-----------------|------------------|-------------------|--------------------------|--------------------|
| 334922  | 2       | havana         | CDS             | 141058883 | 141059054 | .     | -      | 0     | CCDS2182  | NaN             | 9.0         | NaN          | protein_coding | ENSG00000168702 | LRP1B        | havana         | 17           | OTTHUMG00000131799 | 5.0                 | OTTHUMT00000254736 | 2.0                       | ENSP00000374135 | 3.0             | basic       | protein_coding          | ENST00000389484 | LRP1B-001        | havana            | 1                        | 7.0                |
| 619560  | 4       | havana         | CDS             | 48899829  | 48899925  | .     | -      | 0     | CCDS3485  | NaN             | 3.0         | NaN          | protein_coding | ENSG00000145247 | OCIAD2       | ensembl_havana | 11           | OTTHUMG00000128626 | 34.0                | OTTHUMT00000250495 | 1.0                       | ENSP00000273860 | 4.0             | basic       | protein_coding          | ENST00000273860 | OCIAD2-001       | havana            | 1                        | 8.0                |
| 654662  | 4       | ensembl_havana | CDS             | 108748005 | 108748159 | .     | -      | 0     | CCDS54792 | NaN             | 8.0         | NaN          | protein_coding | ENSG00000164089 | ETNPPL       | ensembl_havana | 8            | OTTHUMG00000161036 | 2.0                 | OTTHUMT00000363510 | 1.0                       | ENSP00000427065 | 1.0             | basic       | protein_coding          | ENST00000512646 | ETNPPL-004       | ensembl_havana    | 2                        | 5.0                |
| 897938  | 6       | havana         | exon            | 133837593 | 133837724 | .     | +      | .     | NaN       | ENSE00001673637 | 2.0         | 1.0          | lincRNA        | ENSG00000223586 | LINC01312    | havana         | 5            | OTTHUMG00000015606 | 1.0                 | OTTHUMT00000042289 | 1.0                       | NaN             | NaN             | basic       | lincRNA                 | ENST00000456347 | LINC01312-001    | havana            | 1                        | 5.0                |
| 1544681 | 10      | ensembl        | start_codon     | 102744054 | 102744056 | .     | +      | 0     | CCDS44473 | NaN             | 1.0         | NaN          | protein_coding | ENSG00000166272 | WBP1L        | ensembl_havana | 16           | OTTHUMG00000018968 | 2.0                 | NaN                | NaN                       | NaN             | NaN             | basic       | protein_coding          | ENST00000448841 | WBP1L-201        | ensembl           | 2                        | 5.0                |
| 1562530 | 10      | ensembl_havana | three_prime_utr | 132782037 | 132783480 | .     | +      | .     | CCDS7669  | NaN             | NaN         | NaN          | protein_coding | ENSG00000068383 | INPP5A       | ensembl_havana | 18           | OTTHUMG00000019293 | 5.0                 | OTTHUMT00000051085 | 2.0                       | NaN             | NaN             | basic       | protein_coding          | ENST00000368594 | INPP5A-001       | ensembl_havana    | 1                        | 7.0                |
| 1679065 | 12      | ensembl_havana | CDS             | 101796677 | 101796762 | .     | -      | 0     | NaN       | NaN             | 2.0         | NaN          | protein_coding | ENSG00000111670 | GNPTAB       | ensembl_havana | 14           | OTTHUMG00000170444 | 1.0                 | OTTHUMT00000409191 | 1.0                       | ENSP00000376651 | 4.0             | basic       | protein_coding          | ENST00000392919 | GNPTAB-002       | ensembl_havana    | 1                        | 4.0                |
| 1943558 | 15      | havana         | transcript      | 97370371  | 97521811  | .     | -      | .     | NaN       | NaN             | NaN         | NaN          | lincRNA        | ENSG00000259664 | CTD-2147F2.2 | havana         | 2            | OTTHUMG00000172036 | 2.0                 | OTTHUMT00000416577 | 2.0                       | NaN             | NaN             | basic       | lincRNA                 | ENST00000558621 | CTD-2147F2.2-001 | havana            | 1                        | 2.0                |
| 2199262 | 17      | havana         | exon            | 64506076  | 64506323  | .     | -      | .     | NaN       | ENSE00002732601 | 1.0         | 1.0          | protein_coding | ENSG00000108654 | DDX5         | ensembl_havana | 13           | OTTHUMG00000178936 | 9.0                 | OTTHUMT00000445047 | 1.0                       | NaN             | NaN             | NaN         | nonsense_mediated_decay | ENST00000578400 | DDX5-028         | havana            | 5                        | 5.0                |
| 2500306 | 19      | havana         | exon            | 56158494  | 56158602  | .     | +      | .     | NaN       | ENSE00003648015 | 2.0         | 1.0          | protein_coding | ENSG00000167685 | ZNF444       | ensembl_havana | 14           | OTTHUMG00000181761 | 3.0                 | OTTHUMT00000457506 | 1.0                       | NaN             | NaN             | mRNA_end_NF | processed_transcript    | ENST00000587664 | ZNF444-005       | havana            | 3                        | 5.0                |


So the 10 newly added columns are

```
exon_version
gene_version
havana_gene
havana_gene_version
havana_transcript
havana_transcript_version
protein_version
transcript_biotype
transcript_support_level
transcript_version
```
