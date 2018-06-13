# GTF2CSV

Transform GTF/GFF2 to CSV for your convenience, e.g. insert it into a database
or load it into pandas dataframe for slicing and dicing.

I may do GFF3 later.

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
each tag into its own column. The only troublesome one is the "tag" tag
(unfortunate name), which could appear multiple times per row, e.g.

```
... exon_id "ENSE00001637883"; tag "cds_end_NF"; tag "mRNA_end_NF";
```

I decided to create a binary (1/0) column for each of its corresponding values,
which include

1. `CCDS`
1. `cds_start_NF`
1. `cds_end_NF`
1. `mRNA_start_NF`
1. `mRNA_end_NF`
1. `seleno`
1. `basic` (not appearing in GRCh37.75)

* seleno means that it contains a selenocysteine.
* NF means that it could not be confirmed.

For more details about their meanings, please see
https://www.gencodegenes.org/gencode_tags.html.

At least for the two annotations I tested on, GRCh37.75 and GRCh38.92, "tag" is
the only tag that could appear multiple times. In other GTF files, there could
be other tag with multiplicity above 1, you could check them with the
`check_tag_multiplicity.py` script.

### Usage

The only external package needed is [pandas=>0.18.1](http://pandas.pydata.org/),
whose `read_csv` method could infer compression of input file automatically.

```
python gtf2csv.py [prefix].gtf
```
Output will be saved as `[prefix].csv`.

### Transformed Examples

I have downloaded and transformed two versions of human genome annotations:

```
wget --timestamping http://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/Homo_sapiens.GRCh37.75.gtf.gz
wget --timestamping  ftp://ftp.ensembl.org/pub/release-92/gtf/homo_sapiens/Homo_sapiens.GRCh38.92.gtf.gz
```

For a brief analysis of the transformed files, please see
[EDA.ipynb](https://github.com/zyxue/gtf2csv/blob/master/EDA.ipynb).


### Development

Create a virtual environment:

```
conda env create --prefix venv -f env-conda.yml
```

Start the server

```
jupyter notebook --no-browser --ip 0.0.0.0
```

Export the virtual environment:

```
conda env export --prefix venv > env-conda.yml
```
