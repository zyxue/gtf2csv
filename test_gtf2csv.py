import pandas as pd

from gtf2csv import gtf2df


def test_gtf2csv_for_hg19_sample():
    df0 = pd.read_csv('./test_data/Homo_sapiens.GRCh37.75.head5000.csv',
                      dtype=str)
    df = gtf2df('./test_data/Homo_sapiens.GRCh37.75.head5000.gtf')
    assert df.equals(df0)


def test_gtf2csv_for_hg38_sample():
    # the following field makes the in-memory comparison complicated:
    # transcript_support_level "NA"
    # instead, just compare the long strings
    with open('./test_data/Homo_sapiens.GRCh38.88.head5000.csv', 'rt') as inf:
        expected = inf.read()
    df = gtf2df('./test_data/Homo_sapiens.GRCh38.88.head5000.gtf')
    assert hash(df.to_csv(index=False)) == hash(expected)
