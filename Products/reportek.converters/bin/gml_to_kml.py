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
    GML to KML converter module.
"""


from .kml_generator  import KMLGenerator
from .gml            import GMLStructure
from .gml_parser     import gml_import
from .utils          import utOpen, transcalc
from .constants      import *

from string         import strip

import sys, os, math
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


def gml_to_kml(gml_file):
    #generate name
    name = gml_file[:gml_file.rfind('.')]

    input_gml = utOpen(gml_file)
    conv_gml = GMLStructure()
    conv_gml.setGeo_name(name)

    # fill geometry
    conv_gml = gml_import(input_gml.read(),conv_gml)

    # GML output
    kml_generator = KMLGenerator()

    kml_data = kml_generator.fillKMLHeader()
    kml_data += kml_generator.fillKMLStyle()
    if conv_gml.getFeat_type() == '1':
        for m in range(len(conv_gml.getShp_records())):
            for n in range (len(conv_gml.getShp_records()[m])):
                    x,y = transcalc((conv_gml.getShp_records()[m][n])[0][0],(conv_gml.getShp_records()[m][n])[0][1],10)
                    kml_data += kml_generator.fillKMLPoint("", x, y)
    elif conv_gml.getFeat_type() == '3':
        for m in range(len(conv_gml.getShp_records())):
            thelist = []
            temp_thelist = thelist.append 
            for k in range (len(conv_gml.getShp_records()[m])):
                mylist = []
                temp_mylist = mylist.append 
                for j in ((conv_gml.getShp_records()[m])[k]):
                    temp_mylist(transcalc(j[0],j[1],10))
                temp_thelist(mylist)
            kml_data += kml_generator.fillKMLLine("", thelist)
    elif conv_gml.getFeat_type() == '5':
        for m in range(len(conv_gml.getShp_records())):
            thelist = []
            temp_thelist = thelist.append 
            for k in range (len(conv_gml.getShp_records()[m])):
                mylist = []
                temp_mylist = mylist.append 
                for j in ((conv_gml.getShp_records()[m])[k]):
                    temp_mylist(transcalc(j[0],j[1],10))
                temp_thelist(mylist)
            kml_data += kml_generator.fillKMLPoly("", thelist)
    kml_data += kml_generator.fillKMLFooter()
    return kml_data

if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('--gml')

    try:    options, args = parser.parse_args()
    except: options = None

    if not options or not options.gml:
        print(__doc__)
        print("For help use --help")
    else:
        if sys.platform == "win32":
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(gml_to_kml(gml_file=options.gml))
