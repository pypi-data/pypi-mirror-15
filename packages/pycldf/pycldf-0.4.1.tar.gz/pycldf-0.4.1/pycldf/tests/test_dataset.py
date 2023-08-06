# coding: utf8
from __future__ import unicode_literals, print_function, division

from mock import patch, Mock
from clldutils.testing import WithTempDir
from clldutils.jsonlib import load

from pycldf.tests.util import FIXTURES


class Tests(WithTempDir):
    def test_dataset_from_file(self):
        from pycldf.dataset import Dataset

        ds = Dataset.from_file(FIXTURES.joinpath('ds1.csv'))
        self.assertIn('ds1', repr(ds))
        self.assertEqual(len(ds), 2)
        self.assertEqual(ds.table.url, 'ds1.csv')
        self.assertEqual(ds.metadata['dc:creator'], 'The Author')

        row = ['3', 'abcd1234', 'fid2', 'maybe', '', 'new[4]']
        with self.assertRaises(ValueError):
            ds.add_row(row)

        ds.sources.add('@book{new,\nauthor={new author}}')
        res = ds.add_row(row)
        self.assertEqual(res.url, 'http://example.org/valuesets/3')
        self.assertEqual(len(res.refs), 1)
        self.assertEqual(
            res.valueUrl('Language_ID'),
            'http://glottolog.org/resource/languoid/id/abcd1234')
        out = self.tmp_path()
        ds.write(out, '.tsv')
        self.assertTrue(out.joinpath('ds1.bib').exists())
        md = load(out.joinpath('ds1.tsv-metadata.json'))
        self.assertEqual('ds1.tsv', md['tables'][0]['url'])
        Dataset.from_file(out.joinpath('ds1.tsv'))

    def test_invalid_dataset_from_file(self):
        from pycldf.dataset import Dataset

        log = Mock(warn=Mock())
        with patch('pycldf.dataset.log', log):
            Dataset.from_file(FIXTURES.joinpath('invalid.csv'), skip_on_error=True)
            self.assertEqual(log.warn.call_count, 2)

        with self.assertRaises(ValueError):
            Dataset.from_file(FIXTURES.joinpath('invalid.csv'))

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

    def test_write_read_archive(self):
        from pycldf.dataset import Dataset
        from pycldf.util import Archive

        ds = Dataset.from_file(FIXTURES.joinpath('ds1.csv'))
        out = self.tmp_path()

        with self.assertRaises(ValueError):
            ds.write(out.joinpath('non-existing'), '.tsv', archive=True)

        with Archive(self.tmp_path('archive.zip').as_posix(), 'w') as archive:
            ds.write('.', archive=archive)
            ds2 = Dataset.from_file(FIXTURES.joinpath('ds1.csv'))
            ds2.name = 'new_name'
            ds2.write('.', archive=archive)
        ds_out = Dataset.from_zip(self.tmp_path('archive.zip'), name='ds1')
        self.assertEqual(ds.rows, ds_out.rows)
        self.assertEqual(ds.metadata, ds_out.metadata)

        ds.write(out, '.tsv', archive=True)
        ds_out = Dataset.from_zip(out.joinpath('ds1.zip'))
        self.assertEqual(ds.rows, ds_out.rows)
        self.assertEqual(ds.metadata, ds_out.metadata)

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
