# encoding: utf-8
import unittest
from path import path

rar_data = path(__file__).parent / 'rar_data'


class RarConverterTest(unittest.TestCase):

    def test_rar2list_returns_listing_with_one_file(self):
        from convert import call
        result = call('rar2list', str(rar_data / 'onefile.rar'))
        self.assertIn('fisier.txt', result)
        self.assertIn('04-09-12', result)

    def test_rar2list_with_unicode_characters_returns_contents(self):
        from convert import call
        result = call('rar2list', str(rar_data / 'diacritics.rar'))
        self.assertIn(u"director cu spații și diacritice".encode('utf-8'),
                      result)
