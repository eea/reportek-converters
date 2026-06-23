# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA). Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
# Authors:
# Olimpiu Rob - Eau de Web Romania

__doc__ = """
    XML to JSON converter.
"""

import argparse
import json
import sys
import xmltodict
from lxml import etree
from copy import deepcopy


def clean_metadata(value):
    """Remove XML parser artefacts from metadata extracted by XPath.

    Serialising a selected subtree can add namespace declarations such as
    ``xmlns:xsi`` to the subtree root. xmltodict exposes those declarations as
    ``@xmlns`` keys, but Reportek metadata consumers expect the old clean shape
    without namespace bookkeeping.
    """
    if isinstance(value, dict):
        return {
            key: clean_metadata(item)
            for key, item in value.items()
            if key != "@xmlns"
        }
    if isinstance(value, list):
        return [clean_metadata(item) for item in value]
    return value


def node_to_dict(node):
    """Convert an XML node to the metadata shape expected by Reportek.

    Leaf nodes should become scalar values even if namespace declarations are
    present, otherwise metadata consumers such as get_transaction_year() receive
    a dict and fail when coercing the year to int.
    """
    tag = etree.QName(node).localname
    if len(node) == 0:
        return {tag: (node.text or "")}
    return clean_metadata(
        xmltodict.parse(etree.tostring(node), process_namespaces=True)
    )


def xml_to_json(xml, xpaths):
    tree = etree.parse(xml)
    root = tree.getroot()
    result = {}

    if not xpaths:
        result = xmltodict.parse(etree.tostring(root), process_namespaces=True)
    else:
        for p in xpaths:
            res = []
            for node in root.xpath(p):
                res.append(node_to_dict(node))
            result[p] = res

    return json.dumps(result, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'xml',
        metavar='xml',
        help='path to xml file')
    parser.add_argument(
        '--k',
        metavar='k',
        help='xpath',
        # action='append',
        nargs="*",
        dest='k',
        default=None)
    try:
        args = parser.parse_args()
    except:
        args = None

    if not args or not args.xml:
        print(__doc__)
        print("For help use --help")
    else:
        if sys.platform == "win32":
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(xml_to_json(args.xml, args.k))
