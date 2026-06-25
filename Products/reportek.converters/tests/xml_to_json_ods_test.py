import json
import os
import tempfile
import unittest

from bin.xml_to_json import xml_to_json


class XmlToJsonOdsTest(unittest.TestCase):

    def test_ods_transaction_year_keeps_real_attribute_and_text(self):
        xml = '''<Reporting xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="http://example.invalid/schema.xsd"
            type="ods">
          <GeneralReportData status="submitted" xml:lang="en">
            <TransactionYear valid="true">2025</TransactionYear>
          </GeneralReportData>
        </Reporting>'''
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as tmp:
            tmp.write(xml)
            tmp_path = tmp.name
        try:
            result = json.loads(xml_to_json(tmp_path, ["//TransactionYear"]))
        finally:
            os.unlink(tmp_path)

        self.assertEqual(
            {
                "TransactionYear": {
                    "@valid": "true",
                    "#text": "2025",
                }
            },
            result["//TransactionYear"][0],
        )
        self.assertNotIn("@xmlns", result["//TransactionYear"][0]["TransactionYear"])
