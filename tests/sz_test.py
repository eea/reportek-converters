# encoding: utf-8
import unittest
from path import path


sz_data = path(__file__).parent / 'sz_data'


class SevenZipTest(unittest.TestCase):

    def test_list_7zip_returns_empty_list_for_empty_archive(self):
        from convert import call
        result = call('list_7zip', str(sz_data / 'empty.7z'))
        self.assertIn('0 files, 0 folders', result)

    def test_list_7zip_with_unicode_chars_returns_contents(self):
        from convert import call
        result = call('list_7zip', str(sz_data / 'twofiles.7z'))
        self.assertIn('one.txt', result)
        self.assertIn(u'tw\u0307\u0275.txt'.encode('utf-8'), result)
        self.assertIn('2 files, 0 folders', result)
