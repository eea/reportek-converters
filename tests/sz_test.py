import unittest
from path import path


sz_data = path(__file__).parent / 'sz_data'


class SevenZipTest(unittest.TestCase):

    def test_list_7zip_returns_empty_list_for_empty_archive(self):
        from convert import call
        result = call('list_7zip', str(sz_data / 'empty.7z'))
        self.assertIn('0 files, 0 folders', result)
