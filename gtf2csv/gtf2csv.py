import logging

import pandas as pd

from gtf2csv.args import get_args
from gtf2csv.parsers import (
    get_multiplicity_tags,
    classify_multiplicity_tags,
    parse_attribute_column
)
import gtf2csv.utils as U


logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')


@U.timeit
def read_gtf(filename, cols):
    logging.info(f'reading {filename} ...')
    # http://uswest.ensembl.org/info/website/upload/gff.html
    df = pd.read_csv(
        filename, header=None, names=cols,
        sep='\t', comment='#', dtype=str
    )
    # not sure why it could ends with dtype 'O', enforce them to be int
    for c in ['start', 'end']:
        df[c] = df[c].astype(int)
    return df


def gen_output(input_gtf, output_format):
    if input_gtf.endswith('.gtf'):
        output_csv = input_gtf.replace('.gtf', f'.{output_format}')
    elif input_gtf.endswith('.gtf.gz'):
        output_csv = input_gtf.replace('.gtf.gz', f'.{output_format}')
    else:
        raise ValueError('unknown file extension, must be .gtf or .gtf.gz')
    return output_csv


def gtf2csv(filename, num_cpus, cardinality_cutoff, gtf_cols):
    """
    1. read gtf
    2. extract attributes as separate columns
    3. transform to a pandas dataframe
    """
    df = read_gtf(filename, gtf_cols)

    mlp_tags = get_multiplicity_tags(df.attribute.values, num_cpus)

    lc_tags, hc_tags = classify_multiplicity_tags(
        df.attribute.values, mlp_tags, cardinality_cutoff, num_cpus)

    attr_parsed = parse_attribute_column(
        df.attribute.values, lc_tags, hc_tags, num_cpus)

    logging.info('converting to dataframe...'.format(filename))
    attr_df = U.timeit(pd.DataFrame.from_dict)(attr_parsed)

    df.drop('attribute', axis=1, inplace=True)
    out_df = U.timeit(pd.concat)([df, attr_df], axis=1)
    return out_df


def main():
    args = get_args()
    logging.info(f'will use {args.num_cpus} CPUs for parallel processing')

    gtf_cols = ['seqname', 'source', 'feature', 'start',
                'end', 'score', 'strand', 'frame', 'attribute']
    output = args.output
    if output is None:
        output = gen_output(args.gtf, args.output_format)

    ndf = gtf2csv(args.gtf, args.num_cpus, args.cardinality_cutoff, gtf_cols)

    # sort attribute columns without reordering gtf_cols
    cols = ndf.columns.tolist()
    ncols = len(gtf_cols) - 1    # attribute column is dropped
    sorted_cols = cols[:ncols] + sorted(cols[ncols:])
    odf = ndf[sorted_cols]

    logging.info(f'writing to {output} ...')
    if args.output_format == 'pkl':
        odf.to_pickle(output)
    else:
        odf.to_csv(output, index=False)


if __name__ == "__main__":
    main()
