import logging
import multiprocessing

from collections import Counter, defaultdict

import gtf2csv.utils as U

logger = logging.getLogger(__name__)


def check_multiplicity(attr_str):
    res = []
    attrs = attr_str.strip(';').split(';')
    tags = []
    for attr in attrs:
        tag, _ = parse_attr(attr)  # val is ignored
        tags.append(tag)
    count_dd = Counter(tags)
    for t, n in count_dd.items():
        if n > 1:
            res.append(t)
    return res


@U.timeit
def get_multiplicity_tags(attributes, num_cpus):
    """
    check which tags could appear multiple times per row in the attribute
    column
    """
    logger.info('1st pass of gtf to obtain multiplicity tags ...')

    with multiprocessing.Pool(num_cpus) as p:
        res = p.map(check_multiplicity, attributes, chunksize=10000)

    tags = set(i for j in res for i in j)
    logger.info(f'multiplicity tags found: {tags}')
    return tags


def calc_cardinality_per_row(attr_str, mlp_tags):
    attrs = attr_str.strip(';').split(';')
    res = defaultdict(list)
    for attr in attrs:
        tag, val = parse_attr(attr)
        if tag in mlp_tags:
            res[tag].append(val)
    if len(res) > 0:
        return res


def collect_mlp_tag_val_set(attributes, mlp_tags, num_cpus):
    """collect value set for each multiplicity tag"""
    iters = zip(attributes, [mlp_tags] * len(attributes))
    with multiprocessing.Pool(num_cpus) as p:
        res = p.starmap(calc_cardinality_per_row, iters, chunksize=10000)
        res = [_ for _ in res if _ is not None]

    set_dd = defaultdict(set)
    for dd in res:
        for tag in mlp_tags:
            set_dd[tag].update(dd[tag])
    return set_dd


def do_classification(val_set_dd, card_cutoff):
    hc_tags, lc_tags = [], []
    for tag, val in val_set_dd.items():
        card = len(val)
        if card <= card_cutoff:
            lc_tags.append((tag, card))
        else:
            hc_tags.append((tag, card))

    logger.info((
        f'{len(lc_tags)} low-cardinality tags found: {lc_tags}; '
        f'{len(hc_tags)} high-cardinality tags found: {hc_tags}'
    ))

    # remove cardinality information
    lc_tags = [_[0] for _ in lc_tags]
    hc_tags = [_[0] for _ in hc_tags]
    return lc_tags, hc_tags


@U.timeit
def classify_multiplicity_tags(attributes, mlp_tags, cardinality_cutoff, num_cpus):
    """
    classify multiplicity tags into

    low-caridnaltiy tags (multiplicity <= cardinality_cutoff) and
    high-cardinality tags (multiplicity > cardinality_cutoff)
    """
    logger.info('2nd pass of gtf to classify multiplicity tags into low- and high-cardinality tags ...')
    val_set_dd =  collect_mlp_tag_val_set(attributes, mlp_tags, num_cpus)
    lc_tags, hc_tags = do_classification(val_set_dd, cardinality_cutoff)
    return lc_tags, hc_tags


def parse_attr(attr):
    tag, value = attr.split(maxsplit=1)
    return (tag, value.strip('"'))


def parse_attrs_str(attrs_str, lc_tags, hc_tags):
    """
    "parse a the attribute string for single row

    :params lc_tags: low-cardinality multiplicity tags
    :params hc_tags: high-cardinality multiplicity tags
    """
    # strip: remove last ';'
    attrs = attrs_str.strip(';').split(';')
    res = {}
    for attr in attrs:
        tag, val = parse_attr(attr)
        if tag in lc_tags:
            # convert multiplicity_tag into a binary column
            res[f'{tag}:{val}'] = 1
        elif tag in hc_tags:
            if tag not in res:
                res[tag] = [val]
            else:
                res[tag].append(val)
        else:
            res[tag] = val

    # for high-cardinality tags: join list into string
    for t in hc_tags:
        if t in res:
            res[t] = ','.join(sorted(res[t]))
    return res


@U.timeit
def parse_attribute_column(attributes, lc_tags, hc_tags, num_cpus):
    """
    :params attribute_series: a list of values for the GTF attribute column
    """
    logger.info('3rd pass of gtf to parse the attribute column and convert it into a dataframe ...')
    num = len(attributes)
    params = zip(attributes, [lc_tags] * num, [hc_tags] * num)
    with multiprocessing.Pool(num_cpus) as p:
        res = p.starmap(parse_attrs_str, params, chunksize=20000)
    return res
