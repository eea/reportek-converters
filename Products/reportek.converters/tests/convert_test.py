import unittest
from utils import mime_types
from mock import patch, Mock
from web import create_app


class ConvertTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

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

    @patch('convert.json')
    def test_extraparams_initialisation(self, mock_json):
        mock_json.loads = Mock(return_value=
            [{  "name": "mock_converter",
                "command": "command --arg {0} --extra_arg {1}",
                "accepted_content_types": ["text/xml"],
                "title": "View map as PNG image (thumbnail with background)",
                "returned_content_type": "image/png",
                "extraparams": ["country_code"]
            }]
        )
        from convert import init_converters
        converters = init_converters()
        self.assertEqual(
            ['country_code'],
            converters['mock_converter'].extraparams)

    @patch('convert.json')
    def test_additional_files_param(self, mock_json):
        mock_json.loads = Mock(return_value=
            [{  "name": "mock_converter",
                "command": "command --arg {0} --extra_arg {1}",
                "accepted_content_types": ["text/xml"],
                "title": "View map as PNG image (thumbnail with background)",
                "returned_content_type": "image/png",
                "extraparams": ["country_code"],
                "additional_files": True
            }]
        )
        from convert import init_converters
        converters = init_converters()
        conv = converters['mock_converter']
        self.assertEqual(conv.additional_files, True)
    @patch('web.converters')
    @patch('web.call')
    @patch('convert.json')
    def test_additional_files_passed_as_extra_params(self, mock_json, mock_call, mock_converters):
        mock_json.loads = Mock(return_value=
            [{  "name": "mock_converter",
                "command": "command --arg {0} --extra_arg {1}",
                "accepted_content_types": ["text/xml"],
                "title": "View map as PNG image (thumbnail with background)",
                "returned_content_type": "image/png",
                "extraparams": ["country_code"],
                "additional_files": True
            }]
        )
        import web
        import flask
        from path import path
        from convert import init_converters
        import io

        converters = init_converters()
        mock_converters.get = Mock(return_value=converters['mock_converter'])

        files = {
            'file': (io.StringIO('shp data'), 'file.shp'),
            'shx': (io.StringIO('shx data'), 'file.shx'),
            'dbf': (io.StringIO('dbf data'), 'file.dbf')
        }
        resp = self.client.post("/convert/mock_converter", data=files)
        self.assertEqual(2, len(mock_call.mock_calls[0][1][2]))
        assert path(mock_call.mock_calls[0][1][2][0]).startswith('/tmp/')
        assert path(mock_call.mock_calls[0][1][2][1]).startswith('/tmp/')
