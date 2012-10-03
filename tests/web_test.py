import unittest
import flask
import tempfile
from StringIO import StringIO
from web import create_app


class WebTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home(self):
        resp = self.client.get("/")
        self.assertEqual(200, resp.status_code)

    def test_converters_list(self):
        resp = self.client.get("/list")
        import json
        self.assertIn('rar2list', json.loads(resp.data)['list'])

    def test_converters_params(self):
        """
        Converter params:
            id, title, convert_url, ct_input,
            ct_output, ct_schema, ct_extraparams,
            description, suffix
        """
        with self.app.test_request_context():
            resp = self.client.get("/params")
            import json
            self.assertEqual(
                ['%srar2list' %self.app.config.get('PREFIX', ''), #id
                 'List of contents (%s)' %self.app.config.get('TAG', ''), #title
                 'convert/rar2list', #convert_url
                 'application/x-rar-compressed', #ct_input
                 'text/plain;charset="utf-8"', #ct_output
                 '', #ct_schema
                 [], #ct_extraparams
                 '', #description
                 ''], #suffix
                json.loads(resp.data)['list'][0]
            )
        prefix = self.app.config.get('PREFIX', None)
        if prefix:
            self.assertIn(prefix, json.loads(resp.data).get('prefix'))

    def test_unknown_converter(self):
        data = {}
        data['file'] = (StringIO("file data"), 'file.unk')
        resp = self.client.post("/convert/unknown", data=data)
        self.assertEqual(500, resp.status_code)

    def test_rar2list_exists(self):
        data = {}
        data['file'] = (StringIO("file data"), 'file.rar')
        resp = self.client.post("/convert/rar2list", data=data)
        self.assertEqual(200, resp.status_code)

    def test_rar2list_with_real_file(self):
        data = {}
        with file('tests/rar_data/onefile.rar') as f:
            data['file'] = (f, 'onefile.rar')
            resp = self.client.post("/convert/rar2list", data=data)
            self.assertIn('fisier.txt', resp.data)
