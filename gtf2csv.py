import logging
import multiprocessing
from collections import Counter
import argparse

from tqdm import tqdm
import pandas as pd


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')


# http://uswest.ensembl.org/info/website/upload/gff.html
GTF_COLS = [
    'seqname', 'source', 'feature', 'start',
    'end', 'score', 'strand', 'frame',
    'attribute'
]


def parse_attr(attr):
    tag, value = attr.split(maxsplit=1)
    return (tag, value.strip('"'))


def parse_attrs_str(attrs_str, multiplicity_tags):
    """
    :params multiplicity_tags: a set of tags potentially appearing multiple
    times in one GTF entry
    """
    # strip: remove last ;
    attrs = attrs_str.strip(';').split(';')
    res = {}
    for attr in attrs:
        tag, value = parse_attr(attr)
        # convert multiplicity_tag into a binary column
        if tag in multiplicity_tags:
            res[f'{tag}_{value}'] = 1
        else:
            res[tag] = value
    return res


def parse_attribute_column(attribute_list, multiplicity_tags, num_cpus):
    """
    :params attribute_series: a list of values for the GTF attribute column
    """
    params = []
    # TODO: parallelized but could be memory intensive
    for attr_str in attribute_list:
        params.append((attr_str, multiplicity_tags))

    with multiprocessing.Pool(num_cpus) as p:
        res = p.starmap(parse_attrs_str, params)
    return res


def read_gtf(filename):
    logging.info('reading {0}...'.format(filename))
    df = pd.read_csv(
        filename, header=None, names=GTF_COLS,
        sep='\t', comment='#', dtype=str
    )
    return df


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
    parser.add_argument(
        '-t', '--num-cpus', type=int,
        help='number of cpus for parallel processing, default to all cpus available'
    )
    return parser.parse_args()


def gen_output(input_gtf):
    if input_gtf.endswith('.gtf'):
        output_csv = input_gtf.replace('.gtf', '.csv')
    elif input_gtf.endswith('.gtf.gz'):
        output_csv = input_gtf.replace('.gtf.gz', '.csv')
    else:
        raise ValueError('unknown file extension, must be .gtf or .gtf.gz')
    return output_csv


def check_multiplicity_per(row):
    res = []
    attrs_str = row.attribute
    attrs = attrs_str.strip(';').split(';')
    tags = []
    for attr in attrs:
        tag, value = parse_attr(attr)
        tags.append(tag)
    count_dd = Counter(tags)
    for t, n in count_dd.items():
        if n > 1:
            res.append(t)
    return res


def get_multiplicity_tags(df_gtf, num_cpus):
    """
    check which tags could appear multiple values in the attribute column of
    one gtf entry (e.g. ont, tag)
    """
    params = []
    # TODO: parallelized but could be memory intensive
    for k, row in tqdm(df_gtf.iterrows()):
        params.append(row)

    with multiprocessing.Pool(num_cpus) as p:
        res = p.map(check_multiplicity_per, params)

    tags = set(i for j in res for i in j)
    logging.info(f'multiplicity tags found: {tags}')
    return tags


def main(filename, num_cpus):
    """
    1. read gtf
    2. extract attributes as separate columns
    3. transform to a pandas dataframe
    """
    df = read_gtf(filename)
    mlp_tags = get_multiplicity_tags(df, num_cpus)

    parsed = parse_attribute_column(df.attribute.values, mlp_tags, num_cpus)

    logging.info('converting to dataframe...'.format(filename))
    attr_df = pd.DataFrame.from_dict(parsed)

    df.drop('attribute', axis=1, inplace=True)
    ndf = pd.concat([df, attr_df], axis=1)
    return ndf


if __name__ == "__main__":
    args = get_args()
    gtf_path = args.gtf
    num_cpus = args.num_cpus if args.num_cpus else multiprocessing.cpu_count()
    logging.info(f'will use {num_cpus} CPUs for parallel processing')

    output_csv = args.output
    if output_csv is None:
        output_csv = gen_output(gtf_path)

    ndf = main(gtf_path, num_cpus)

    # sort attribute columns without reordering GTF_COLS
    cols = ndf.columns.tolist()
    lcol = len(GTF_COLS) - 1  # attribute column is dropped
    sorted_cols = cols[:lcol] + sorted(cols[lcol:])

    logging.info('writing to {0}...'.format(output_csv))
    ndf.to_csv(output_csv, index=False)
