import argparse

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


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert GTF file to plain csv')
    parser.add_argument(
        '-f', '--gtf', type=str, required=True,
        help='the GTF file to convert'
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help=('the output filename, if not specified, would just set it to be '
              'the same as the input but with extension replaced (gtf => csv)')
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    gtf_path = args.gtf

    output_csv = args.output
    if output_csv is None:
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
