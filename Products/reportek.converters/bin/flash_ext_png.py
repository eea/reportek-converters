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
GML to PNG converter INFO.
"""

from gml_image  import gml_to_image, flash_ext_print
from utils      import utOpen, zip_generator
from constants  import *

import sys, os
import optparse
try:
    import msvcrt
except:
    pass


def flash_ext_png(minx, miny, maxx, maxy, gml_file, server = IMS_SERVER, service = IMS_SERVICE):
    # Parse GML/generate PNG with background

    #generate name
    name_tmp = os.path.split(gml_file)[1]
    name = name_tmp[:name_tmp.rfind('.')]

    return flash_ext_print(name, gml_file, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_TYPE , OUTLINE_RGB, FILL_RGB, minx, miny, maxx, maxy, server, service, 1)


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('--minx')
    parser.add_option('--miny')
    parser.add_option('--maxx')
    parser.add_option('--maxy')
    parser.add_option('--gml')
    parser.add_option('--server')
    parser.add_option('--service')


    try:    options, args = parser.parse_args()
    except: options = None

    if not options or not options.gml:
        print __doc__
        print "For help use --help"
    else:
        if sys.platform == "win32":
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(flash_ext_png(minx=options.minx, miny=options.miny, maxx=options.maxx, maxy=options.maxy, gml_file=options.gml, server=options.server, service=options.service))
