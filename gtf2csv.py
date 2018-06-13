import sys

import pandas as pd


# http://uswest.ensembl.org/info/website/upload/gff.html
GTF_COLS = [
    'seqname', 'source', 'feature', 'start',
    'end', 'score', 'strand', 'frame',
    'attribute'
]


def parse_attr(attr):
    tag, value = attr.split(maxsplit=1)
    return (tag, value.strip('"'))


def parse_attrs_str(attrs_str):
    # strip: remove last ;
    attrs = attrs_str.strip(';').split(';')
    res = {}
    for attr in attrs:
        tag, value = parse_attr(attr)
        # since there could be multiple tags per row,
        # e.g. `... tag "cds_end_NF"; tag "mRNA_end_NF";`

        # I verified that only tag is the tag that may appear multiple times
        # per row, so I decided to use the binary (1/0) columns based on the
        # value of tag
        if tag == "tag":
            res[value] = 1
        else:
            res[tag] = value
    return res


def read_gtf(filename):
    print('reading {0}...'.format(filename))
    df = pd.read_csv(
        filename, header=None, names=GTF_COLS,
        sep='\t', comment='#', dtype=str
    )
    return df


def main(filename):
    """
    1. read gtf
    2. extract attributes as separate columns
    3. transform to a pandas dataframe
    """
    df = read_gtf(filename)

    print('converting to dataframe...'.format(filename))
    attr_df = pd.DataFrame.from_dict(
        df.attribute.apply(parse_attrs_str).values.tolist())
    df.drop('attribute', axis=1, inplace=True)
    ndf = pd.concat([df, attr_df], axis=1)
    return ndf


if __name__ == "__main__":
    gtf_path = sys.argv[1]

    if gtf_path.endswith('.gtf'):
        output_csv = gtf_path.replace('.gtf', '.csv')
    elif gtf_path.endswith('.gtf.gz'):
        output_csv = gtf_path.replace('.gtf.gz', '.csv')
    else:
        raise ValueError('unknown file extension, must be .gtf or .gtf.gz')

    ndf = main(gtf_path)

    # sort attribute columns without reordering GTF_COLS
    cols = ndf.columns.tolist()
    lcol = len(GTF_COLS) - 1  # attribute column is dropped
    sorted_cols = cols[:lcol] + sorted(cols[lcol:])

    print('writing to {0}...'.format(output_csv))
    ndf.to_csv(output_csv, index=False)
