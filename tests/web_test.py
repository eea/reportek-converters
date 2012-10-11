import unittest
import flask
import tempfile
import sys
from StringIO import StringIO
from web import create_app

class WebTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def assertInResponse(self, text, filename):
        """ the caller function must be named test_<converter_id> """
        data = {}
        converter_id = sys._getframe(1).f_code.co_name[5:]
        with file(filename) as f:
            data['file'] = (f, 'test.ppt')
            resp = self.client.post("/convert/%s" %converter_id, data=data)
            self.assertIn(text, resp.data)

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
            self.assertIn(
                ['%srar2list' %self.app.config.get('PREFIX', ''), #id
                 'List of contents (%s)' %self.app.config.get('TAG', ''), #title
                 'convert/rar2list', #convert_url
                 'application/x-rar-compressed', #ct_input
                 'text/plain;charset="utf-8"', #ct_output
                 '', #ct_schema
                 [], #ct_extraparams
                 '', #description
                 ''], #suffix
                json.loads(resp.data)['list']
            )
        prefix = self.app.config.get('PREFIX', None)
        if prefix:
            self.assertIn(prefix, json.loads(resp.data).get('prefix'))

    def test_unknown_converter(self):
        data = {}
        data['file'] = (StringIO("file data"), 'file.unk')
        resp = self.client.post("/convert/unknown", data=data)
        self.assertEqual(500, resp.status_code)

    def test_rar2list(self):
        self.assertInResponse('fisier.txt', 'tests/rar_data/onefile.rar')

    def test_pdftohtml(self):
        self.assertInResponse('Flask&#160;Documentation', 'tests/pdf_data/sample.pdf')

    def test_gmltopng_thumb(self):
        self.assertInResponse('PNG', 'tests/gml_data/world.gml')

    def test_msxls2html(self):
        self.assertInResponse('test file', 'tests/xls_data/test.xls')

    def test_vndmsxls2html(self):
        self.assertInResponse('test file', 'tests/xls_data/test.xls')

    def test_xsl2html(self):
        self.assertInResponse('test file', 'tests/xls_data/test.xls')

    def test_ppt2html(self):
        self.assertInResponse('pptHtml', 'tests/ppt_data/test.ppt')

    def test_vndmsppt2html(self):
        self.assertInResponse('pptHtml', 'tests/ppt_data/test.ppt')

    def test_ziplist(self):
        self.assertInResponse('fisier.txt', 'tests/zip_data/test.zip')
