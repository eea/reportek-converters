import unittest
from convert import Converter
from utils import mime_type


class ConvertTest(unittest.TestCase):

    def test_convert_object(self):
        converter = Converter('rar2list', 'unrar l %s', mime_type('rar'))
        self.assertEqual('rar2list', converter.name)
        self.assertEqual('unrar l %s', converter.command)
        self.assertEqual(["application/x-rar-compressed"],
                         converter.accepted_content_types)
        self.assertEqual(converter.returned_content_type,
                         'text/plain;charset="utf-8"')

    def test_converters(self):
        from convert import converters
        converter = Converter('rar2list', 'unrar l %s', mime_type('rar'))
        self.assertEqual(converter.command, converters['rar2list'].command)
