import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='Convert GTF file to plain csv')

    parser.add_argument(
        '-f', '--gtf', type=str, required=True,
        help='the GTF file to convert'
    )

    parser.add_argument(
        '-c', '--cardinality-cutoff', type=int, default=100,
        help=('for a tag that may appear multiple times in the attribute '
              'column (so-called multiplicity tag in this program), '
              'if its cardinality, i.e. the number of possibles values '
              'across all row, is lower than this cutoff, then it\'s a low-caridnaltiy tag, and each of its '
              'possible value would be transformed into a separate binary '
              'column. Otherwise, it is a high-cardinality tag and all of its values in one row would be simply '
              'concatenated to avoid making too many columns')
    )

    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help=('the output filename, if not specified, would just set it to be '
              'the same as the input but with extension replaced (gtf => csv)')
    )

    parser.add_argument(
        '-m', '--output-format', type=str, default='csv', choices=['csv', 'pkl'],
        help=('pkl means python pickle format, which would results in much faster IO (recommended)')
    )

    parser.add_argument(
        '-t', '--num-cpus', type=int, default=1,
        help='number of cpus for parallel processing, default to 1'
    )
    return parser.parse_args()
