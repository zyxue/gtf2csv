import sys
from collections import Counter

"""
Check what tags in the attribute column could appear multiple times per row
in GTF

Of the two versions of GTF I checked, only the tag "tag" could appear multiple
times per row
"""


from gtf2csv import read_gtf, parse_attr


gtf_filename = sys.argv[1]

df = read_gtf(gtf_filename)

multi_tags = set()
for k, row in df.iterrows():
    attrs_str = row.attribute
    attrs = attrs_str.strip(';').split(';')
    tags = []
    for attr in attrs:
        tag, value = parse_attr(attr)
        tags.append(tag)
    count_dd = Counter(tags)
    for t, n in count_dd.items():
        if n > 1:
            multi_tags.add(t)
    if (k + 1) % 10000 == 0:
        print('processed {0} rows'.format(k + 1))

print("tags with multiplicity > 1 include:\n{0}".format(
    ' '.join(sorted(multi_tags)))
)
