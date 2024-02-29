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
                res.append(xmltodict.parse(etree.tostring(node),
                                           process_namespaces=True))
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
