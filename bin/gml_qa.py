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
GML QA module
"""

from gml              import GMLStructure
from gml_geometry     import isPointInsideRectangle
from gml_generator  import GMLGenerator
from gml_sd_parser    import gml_sd_import
from gml_meta_parser  import meta_import
from gml_prj_parser  import prj_import
from gml_parser       import gml_import
from utils            import utOpen, zip_generator
from constants        import *

import sys, os
import optparse
try:
    import msvcrt
except:
    pass

QA_TEMPLATE = """
<div class="feedbacktext">
      <h2>The following quality check was made against this file.</h2>
         <h2>1. GML geometry</h2>
         <p>This rule checks that the GML features are inside the terrestrial country bounding box.</p>
         <ul>
         <li>Number of features verified: %s</li>
         <li>Number of features that are inside the bounding box: %s</li>
         <li>Number of features that are outside the bounding box: %s</li>
         <li>The test was <em>%s</em>.</li>
         </ul>
         <div class="system-msg">If your projection is different from ETRS89-LAEA, the QA test will always report failure</div>
</div>
"""
#total, ok, not ok , passed successfully/not passed

def gml_qa(country_code, gml_file):

    #file read
    input_gml = utOpen(gml_file)

    conv_gml = GMLStructure()

    #fill geometry
    conv_gml = gml_import(input_gml.read(),conv_gml)

    if str(country_code).upper() not in COUNTRIES_DICT:
        country_code = 'EU'
    country_code = str(country_code).upper()
    minx = float(COUNTRIES_DICT[country_code]['minx'])
    miny = float(COUNTRIES_DICT[country_code]['miny'])
    maxx = float(COUNTRIES_DICT[country_code]['maxx'])
    maxy = float(COUNTRIES_DICT[country_code]['maxy'])

    total_number = len(conv_gml.getShp_records())
    bad_feaures = 0
    mark_bad = 0

    if conv_gml.getFeat_type() == '1':
        for m in range(len(conv_gml.getShp_records())):
            for n in range (len(conv_gml.getShp_records()[m])):
                if not isPointInsideRectangle (minx,maxy,maxx,miny,(conv_gml.getShp_records()[m][n])[0][0],(conv_gml.getShp_records()[m][n])[0][1]):
                    mark_bad = 1
            if mark_bad:
                bad_feaures += 1
                mark_bad = 0
    elif conv_gml.getFeat_type() == '3':
        for m in range(len(conv_gml.getShp_records())):
            for k in range (len(conv_gml.getShp_records()[m])):
                for j in ((conv_gml.getShp_records()[m])[k]):
                    if not  isPointInsideRectangle (minx,maxy,maxx,miny,j[0],j[1]):
                        mark_bad = 1
            if mark_bad:
                bad_feaures += 1
                mark_bad = 0
    elif conv_gml.getFeat_type() == '5':
        for m in range(len(conv_gml.getShp_records())):
            for k in range (len(conv_gml.getShp_records()[m])):
                for j in ((conv_gml.getShp_records()[m])[k]):
                    if not isPointInsideRectangle (minx,maxy,maxx,miny,j[0],j[1]):
                        mark_bad = 1
            if mark_bad:
                bad_feaures += 1
                mark_bad = 0

    returnQA = QA_TEMPLATE % (total_number,str(total_number-bad_feaures), bad_feaures,("not passed", "passed successfully")[bad_feaures == 0])


    return returnQA


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('--country')
    parser.add_option('--gml')

    try:    options, args = parser.parse_args()
    except: options = None

    if not options or not options.gml:
        print __doc__
        print "For help use --help"
    else:
        if sys.platform == "win32":
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(gml_qa(country_code=options.country, gml_file=options.gml))

