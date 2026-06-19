# encoding: utf-8
import shutil
import subprocess
import unittest
from path import Path

rar_data = Path(__file__).parent / 'rar_data'


def has_working_binary(name):
    if not shutil.which(name):
        return False
    try:
        result = subprocess.run([name], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=5)
    except Exception:
        return False
    return result.returncode >= 0


@unittest.skipUnless(has_working_binary('unrar'), 'missing working unrar binary')
class RarConverterTest(unittest.TestCase):

    def test_rar2list_returns_listing_with_one_file(self):
        from convert import call
        result = call('rar2list', str(rar_data / 'onefile.rar'))
        self.assertIn('fisier.txt', result)
        self.assertIn('04-09-12', result)

    def test_rar2list_with_unicode_characters_returns_contents(self):
        from convert import call
        result = call('rar2list', str(rar_data / 'diacritics.rar'))
        self.assertIn("director cu spații și diacritice".encode('utf-8'),
                      result)
