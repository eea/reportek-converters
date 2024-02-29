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
# Alexandru Ghica, Finsiel Romania
# Bogdan Grama, Finsiel Romania
# Iulian Iuga, Finsiel Romania

__doc__ = """
    SHP to GML converter module.
"""

import shapelib
import dbflib

from .gml_generator  import GMLGenerator
from .gml_sd_parser  import gml_sd_import
from .gml_meta_parser  import meta_import
from .utils          import utOpen
from .constants      import *

import sys, os
import optparse


def shp_to_gml(filename, in_schema, user_enc="utf-8", temp_name=None):
    #generate name
    name_tmp = os.path.split(filename)[1]
    if '.' in name_tmp:
        name = name_tmp[:name_tmp.rfind('.')]
    else:
        name = name_tmp

    if temp_name:
        meta_filename = temp_name
    else:
        meta_filename = name

    # Creates the GML file
    inputfilepath = os.path.join(FILES_PATH, filename)

    shp = shapelib.ShapeFile(inputfilepath)
    dbf = dbflib.DBFFile(inputfilepath)

    # GML output
    gml_generator = GMLGenerator(user_enc)

    # Some alias
    shp_read = shp.read_object

    #file read
    if not in_schema:
        in_schema = XSD_FILE
    input_schema = utOpen(in_schema)
    # Fill schema(dbf) information
    conv_gml = gml_sd_import(input_schema.read())



    #Read metadata
    retMetadata = {}
    try:
        input_metadata = utOpen("%s.xml" % os.path.join(FILES_PATH, name))
        retMetadata = meta_import(input_metadata.read())
    except:
        for k in METADATA_LABELS:
            retMetadata[k] = ''

    #Read projection
    try:
        input_prj = utOpen("%s.prj" % os.path.join(FILES_PATH, name)).read()
    except:
        input_prj = ''

    dbf_filter = {}
    for j in range(len(conv_gml.getRec_dbf())):
        ttype, tname, tlen, tdecc = (conv_gml.getRec_dbf())[j]
        dbf_filter[tname] = {'type':ttype, 'len':tlen, 'decc':tdecc}

    gml_data = gml_generator.fillHeader(in_schema)
    gml_data += gml_generator.fillMetadata(retMetadata, meta_filename)
    gml_data += gml_generator.fillProjection(input_prj)
    gml_data += gml_generator.fillBoundingBox(shp.info()[2][0], shp.info()[2][1], shp.info()[3][0], shp.info()[3][1])
    for j in range(dbf.record_count()):
        dbf_ready = {}
        for k,v in (list((dbf.read_record(j)).items())):
            if k in dbf_filter:
                if dbf_filter[k]['type'] == 'string':
                    if len(v) is not 0:
                        if len(v) > int(dbf_filter[k]['len']):
                            v = v[:int(dbf_filter[k]['len'])]
                if dbf_filter[k]['type'] == 'decimal':
                    if not len(str(v)) == 0:
                        if not '.' in str(v):
                            v = float(str(v) + ".0")
                        whole,decimal = str(v).split('.')
                        if len(whole) > int(dbf_filter[k]['len']):
                            whole = whole[:int(dbf_filter[k]['len'])]
                        if len(decimal) > int(dbf_filter[k]['decc']):
                            decimal = decimal[:int(dbf_filter[k]['decc'])]
                        v = whole + '.' + decimal
                if dbf_filter[k]['type'] == 'integer':
                    if not len(v) == 0:
                        if len(v) > int(dbf_filter[k]['len']):
                            v = v[:int(dbf_filter[k]['len'])]
                dbf_ready[k] = v
        # Add rest of the records as null
        for kf in dbf_filter:
            if kf not in dbf_ready:
                    dbf_ready[kf] = ''


        # Geometry types
        # Point
        if shp.info()[1] == 1:
            gml_data += gml_generator.fillFeatureMemberPoint("F%s" % j, shp_read(j).vertices()[0][0], shp_read(j).vertices()[0][1], dbf_ready)
        # Polyline
        elif shp.info()[1] == 3:
            gml_data += gml_generator.fillFeatureMemberLine("F%s" % j, shp_read(j).vertices(), dbf_ready)
        # Polygon
        elif shp.info()[1] == 5:
            gml_data += gml_generator.fillFeatureMemberPolygon("F%s" % j, shp_read(j).vertices(), dbf_ready)
    gml_data += gml_generator.fillFooter()

    shp.close()
    dbf.close()

    return gml_data


if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option('--filename')
    parser.add_option('--schema')

    try:    options, args = parser.parse_args()
    except: options = None

    if not options or not options.filename:
        print(__doc__)
        print("For help use --help")
    else:
        sys.stdout.write(shp_to_gml(filename=options.filename, in_schema=options.schema))
