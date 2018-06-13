import sys

"""
Check what values are there for the tag "tag" (unfortunate name)
"""


from gtf2csv import read_gtf, parse_attr


gtf_filename = sys.argv[1]

df = read_gtf(gtf_filename)

tag_values = set()
for k, row in df.iterrows():
    attrs_str = row.attribute
    attrs = attrs_str.strip(';').split(';')
    for attr in attrs:
        tag, value = parse_attr(attr)
        if tag == "tag":
            tag_values.add(value)
    if (k + 1) % 10000 == 0:
        print('processed {0} rows'.format(k + 1))

print("tags with multiplicity > 1 include:\n{0}".format(
    ' '.join(sorted(tag_values)))
)
