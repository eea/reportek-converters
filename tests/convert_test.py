import unittest
from utils import mime_types
from mock import patch, Mock


class ConvertTest(unittest.TestCase):

    def test_convert_object(self):
        from convert import Converter
        converter = Converter('rar2list', 'unrar l {0}', mime_types.get('rar'))
        self.assertEqual('rar2list', converter.name)
        self.assertEqual('unrar l {0}', converter.command)
        self.assertEqual(["application/x-rar-compressed"],
                         converter.accepted_content_types)
        self.assertEqual(converter.returned_content_type,
                         'text/plain;charset="utf-8"')

    def test_converters(self):
        from convert import converters, Converter
        converter = Converter('rar2list', 'unrar l {0}', mime_types.get('rar'))
        self.assertEqual(converter.command, converters['rar2list'].command)
