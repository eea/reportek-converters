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
