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
    GML to SHP converter module.
"""

import shapelib
import dbflib

from .gml              import GMLStructure
from .gml_generator  import GMLGenerator
from .gml_sd_parser    import gml_sd_import
from .gml_meta_parser  import meta_import
from .gml_prj_parser  import prj_import
from .gml_parser       import gml_import
from .utils            import utOpen, zip_generator
from .constants        import *

import sys, os
import optparse
try:
    import msvcrt
except:
    pass

# Allow only 30 seconds of CPU time (Linux only)
try:
    import resource
    resource.setrlimit(resource.RLIMIT_CPU,(30,30))
except:
    pass



def gml_to_shp(gml_file, schema_file, user_enc="utf-8"):

    #generate name
    name_tmp = os.path.split(gml_file)[1]
    if '.' in name_tmp:
        name = name_tmp[:name_tmp.rfind('.')]
    else:
        name = name_tmp


    #file read
    input_gml = utOpen(gml_file)
    if not schema_file:
        schema_file = XSD_FILE
    input_schema = utOpen(schema_file)

    conv_gml = GMLStructure()

    #fill schema(dbf) information
    try:
        conv_gml = gml_sd_import(input_schema.read())
    except Exception as strerror:
        return "", strerror

    conv_gml.setGeo_name(name)

    #fill geometry
    conv_gml = gml_import(input_gml.read(),conv_gml)

    #generate output path
    output_path = os.path.join(FILES_PATH, conv_gml.getGeo_name())

    #prepare outfile
    #SHP Point
    if conv_gml.getFeat_type() == '1':
        outfile = shapelib.create(output_path, shapelib.SHPT_POINT)
        for m in range(len(conv_gml.getShp_records())):
            vertices_up = []
            temp_a = vertices_up.append
            for n in range (len(conv_gml.getShp_records()[m])):
                    temp_a((conv_gml.getShp_records()[m][n]))
#                   print vertices_up
            obj = shapelib.SHPObject(shapelib.SHPT_POINT, 1,vertices_up)
            outfile.write_object(-1, obj)
    #SHP Line
    elif conv_gml.getFeat_type() == '3':
        outfile = shapelib.create(output_path, shapelib.SHPT_ARC)
        for m in range(len(conv_gml.getShp_records())):
            vertices_up = []
            temp_a = vertices_up.append
            for n in range (len(conv_gml.getShp_records()[m])):
                    temp_a((conv_gml.getShp_records()[m][n]))
            obj = shapelib.SHPObject(shapelib.SHPT_ARC, len(vertices_up),vertices_up)
            outfile.write_object(-1, obj)
    #SHP Poligon
    elif conv_gml.getFeat_type() == '5':
        outfile = shapelib.create(output_path, shapelib.SHPT_POLYGON)
        for m in range(len(conv_gml.getShp_records())):
            vertices_up = []
            temp_a = vertices_up.append
            for n in range (len(conv_gml.getShp_records()[m])):
                temp_a(conv_gml.getShp_records()[m][n])
            obj = shapelib.SHPObject(shapelib.SHPT_POLYGON, 1,vertices_up)
            outfile.write_object(-1, obj)
    else:
        outfile = shapelib.create(output_path, shapelib.SHPT_POINT)
        outfile.write_object(-1, shapelib.SHPObject(shapelib.SHPT_POINT, 1, [[(-9999,-9999)]]))

    del outfile

    dbf_recc_type = {}
    dbf_float_decc = {}
    dbf = dbflib.create(output_path)

    dbf.add_field("FID", dbflib.FTInteger, int(8), int(0))
    for j in range(len(conv_gml.getRec_dbf())):
        ttype, tname, tlen, tdecc = (conv_gml.getRec_dbf())[j]
        if ttype == 'string':
            dbf.add_field(tname, dbflib.FTString, int(tlen), int(tdecc))
        elif ttype == 'integer':
            dbf.add_field(tname, dbflib.FTInteger, int(tlen), int(tdecc))
        elif ttype == 'decimal':
            dbf.add_field(tname, dbflib.FTDouble, int(tlen), int(tdecc))
        dbf_recc_type[tname] = ttype
        dbf_float_decc[tname] = tdecc

    # Records added as a dictionary...
    for k in range(len(conv_gml.getDbf_records())):
        recdbf_toadd = {}
        recdbf_toadd["FID"] = int(k)
        for l in range (len(conv_gml.getDbf_records()[k])):
            ntag, valtag = conv_gml.getDbf_records()[k][l]
            if valtag == 'null':
                valtag = ''
            if dbf_recc_type[ntag] == 'integer':
                if valtag == 'None' or valtag == '':
                    recdbf_toadd[ntag] = int()
                else:
                    recdbf_toadd[ntag] = int(valtag)
            elif dbf_recc_type[ntag] == 'decimal':
                if valtag == 'None' or valtag == '':
                    recdbf_toadd[ntag] = float()
                else:
                    recdbf_toadd[ntag] = float(valtag)
            elif dbf_recc_type[ntag] == 'string':
                recdbf_toadd[ntag] = str(valtag)
        dbf.write_record(k, recdbf_toadd)
        recdbf_toadd.clear 
    dbf.close()

    #Fill metadata
    gml_generator = GMLGenerator(user_enc)
    input_metadata = utOpen(gml_file)
    retMetadata = meta_import(input_metadata.read())

    l_file = open(os.path.join(FILES_PATH, '%s%s' % (name, '.xml')), 'wb')
    l_file.write(gml_generator.fillExportMetadata(retMetadata, name))
    l_file.close()

    #Fill projection
    input_prj = utOpen(gml_file)
    retProjection = prj_import(input_prj.read())

    l_file = open(os.path.join(FILES_PATH, '%s%s' % (name, '.prj')), 'wb')
    l_file.write(str(retProjection))
    l_file.close()

    res = zip_generator(FILES_PATH, name)

    #delete the shapelib files
    for k in EXTENSIONS:
        try:
            os.unlink(os.path.join(FILES_PATH, '%s%s' % (name, k)))
        except Exception as msg:
            print(msg)

    return res


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('--gml')
    parser.add_option('--schema')

    try:    options, args = parser.parse_args()
    except: options = ""

    if not options or not options.gml:
        print(__doc__)
        print("For help use --help")
    else:
        if sys.platform == "win32":
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(gml_to_shp(gml_file=options.gml, schema_file=options.schema))
