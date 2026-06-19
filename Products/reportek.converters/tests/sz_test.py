# encoding: utf-8
import shutil
import subprocess
import unittest
from path import Path


sz_data = Path(__file__).parent / 'sz_data'


def has_working_binary(name):
    if not shutil.which(name):
        return False
    try:
        result = subprocess.run([name], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=5)
    except Exception:
        return False
    return result.returncode >= 0


@unittest.skipUnless(has_working_binary('7za'), 'missing working 7za binary')
class SevenZipTest(unittest.TestCase):

    def test_list_7zip_returns_empty_list_for_empty_archive(self):
        from convert import call
        result = call('list_7zip', str(sz_data / 'empty.7z'))
        self.assertIn('0 files, 0 folders', result)

    def test_list_7zip_with_unicode_chars_returns_contents(self):
        from convert import call
        result = call('list_7zip', str(sz_data / 'twofiles.7z'))
        self.assertIn('one.txt', result)
        self.assertIn('2 files, 0 folders', result)
