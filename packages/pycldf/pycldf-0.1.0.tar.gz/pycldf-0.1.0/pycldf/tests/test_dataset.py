# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir
from clldutils.path import Path


FIXTURES = Path(__file__).parent.joinpath('fixtures')


class Tests(WithTempDir):
    def test_dataset_from_file(self):
        from pycldf.dataset import Dataset

        ds = Dataset.from_file(FIXTURES.joinpath('ds1.csv'))
        self.assertEqual(len(ds), 2)
        self.assertEqual(ds.source_count()['meier2015'], 1)
        self.assertEqual(ds.source_count()['80086'], 2)
        self.assertEqual(ds.metadata['dc:creator'], 'The Author')

        row = ['3', 'abcd1234', 'fid2', 'maybe', '', 'new[4]']
        with self.assertRaises(AssertionError):
            ds.add_row(row)

        ds.sources.add('@book{new,\nauthor={new author}}')
        ds.add_row(row)

        out = self.tmp_path()
        ds.write(out, '.tsv')
        self.assertTrue(out.joinpath('ds1.bib').exists())
        Dataset.from_file(out.joinpath('ds1.tsv'))

    def test_write_read(self):
        from pycldf.dataset import Dataset, REQUIRED_FIELDS

        row = ['1', 'abcd1234', 'fid', 'yes']
        ds = Dataset('name')
        ds.fields = tuple(v[0] for v in REQUIRED_FIELDS)
        ds.add_row(row)
        ds.write(self.tmp_path())
        self.assertTrue(self.tmp_path('name.csv').exists())
        ds2 = Dataset.from_file(self.tmp_path('name.csv'))
        self.assertEqual(list(ds2[0].values()), row)
        self.assertEqual(list(ds2['1'].values()), row)

    def test_validate(self):
        from pycldf.dataset import Dataset, REQUIRED_FIELDS

        ds = Dataset('name')
        with self.assertRaises(AssertionError):  # missing required fields!
            ds.fields = ('a',)

        with self.assertRaises(AssertionError):  # fields must be tuple
            ds.fields = [variants[-1] for variants in REQUIRED_FIELDS]

        ds.fields = tuple(variants[-1] for variants in REQUIRED_FIELDS)

        with self.assertRaises(ValueError):  # fields cannot be reassigned!
            ds.fields = tuple(variants[0] for variants in REQUIRED_FIELDS)
