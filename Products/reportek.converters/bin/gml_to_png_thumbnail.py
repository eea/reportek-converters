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
    GML to PNG_thumbnail converter module.
"""

from .gml_image      import gml_to_image
from .utils          import utOpen, zip_generator
from .constants      import *

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

def gml_to_png_thumb(gml_file):
    # Parse GML/generate PNG_thumbnail

    #generate name
    name_tmp = os.path.split(gml_file)[1]
    name = name_tmp[:name_tmp.rfind('.')]

    return gml_to_image(name, gml_file, IMAGE_WIDTH_TH, IMAGE_HEIGHT_TH, IMAGE_TYPE , OUTLINE_RGB, FILL_RGB, "", "", "", 0)


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
        sys.stdout.write(gml_to_png_thumb(gml_file=options.gml))
