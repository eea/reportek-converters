import json
import os
import tempfile
import unittest

from bin.xml_to_json import xml_to_json


class XmlToJsonTest(unittest.TestCase):

    def convert(self, xml, xpaths):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as tmp:
            tmp.write(xml)
            tmp_path = tmp.name
        try:
            return json.loads(xml_to_json(tmp_path, xpaths))
        finally:
            os.unlink(tmp_path)

    def test_selected_leaf_nodes_without_real_attributes_are_scalars(self):
        result = self.convert(
            '<Root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<Alpha>2024</Alpha><Beta>two</Beta>'
            '</Root>',
            ["//Alpha", "//Beta"],
        )

        self.assertEqual({"Alpha": "2024"}, result["//Alpha"][0])
        self.assertEqual({"Beta": "two"}, result["//Beta"][0])

    def test_selected_leaf_nodes_with_real_attributes_keep_text_marker(self):
        result = self.convert(
            '<Root><Alpha valid="true">2024</Alpha></Root>',
            ["//Alpha"],
        )

        self.assertEqual(
            {"Alpha": {"@valid": "true", "#text": "2024"}},
            result["//Alpha"][0],
        )

    def test_selected_parent_nodes_keep_nested_structure(self):
        result = self.convert(
            '<Root><Gamma><Delta>three</Delta></Gamma></Root>',
            ["//Gamma"],
        )

        self.assertEqual(
            {"Gamma": {"Delta": "three"}},
            result["//Gamma"][0],
        )

    def test_selected_subtrees_do_not_include_namespace_declarations(self):
        result = self.convert(
            '<Root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<Gamma><Delta xsi:nil="true" /></Gamma>'
            '</Root>',
            ["//Gamma"],
        )

        self.assertNotIn("@xmlns", result["//Gamma"][0]["Gamma"])
