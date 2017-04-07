import sys

import pandas as pd


def clean_attr(attr):
    name, value = attr.split(maxsplit=1)
    return (name, value.strip('"'))


def parse_attrs(attrs_str):
    # strip: remove last ;
    attrs = attrs_str.strip(';').split(';')
    return dict([clean_attr(_) for _ in attrs])


def get_column_names(input_annot):
    if input_annot.endswith('.gtf'):
        # http://uswest.ensembl.org/info/website/upload/gff.html
        column_names = [
            'seqname', 'source', 'feature', 'start', 'end',
            'score', 'strand', 'frame', 'attribute'
        ]
    else:
        raise ValueError(
            'cannot decide the columns based on the file '
            'suffix\n{0}\n, please specify them'.format(input_annot))
    return column_names


def gtf2df(input_annot, column_names=None):
    """
    1. read gtf
    2. extract attributes as separate columns
    3. transform to a pandas dataframe
    """
    print('reading {0}...'.format(input_annot))
    if column_names is None:
        column_names = get_column_names(input_annot)
    df = pd.read_csv(input_annot, header=None, names=column_names,
                     sep='\t', comment='#', dtype=str)

    print('converting to dataframe...'.format(input_annot))
    attr_df = pd.DataFrame.from_dict(
        df.attribute.apply(parse_attrs).values.tolist())

    ndf = pd.concat([df.drop('attribute', axis=1), attr_df], axis=1)
    return ndf


if __name__ == "__main__":
    input_annot = sys.argv[1]
    output_csv = input_annot.replace('.gtf', '.csv')

    ndf = gtf2df(input_annot)

    print('writing to {0}...'.format(output_csv))
    ndf.to_csv(output_csv, index=False)
