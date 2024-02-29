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
      File management for conversion process(move to temporary folder and cleanup)
"""

import shapelib
import dbflib
import shptree
import io
import sys
import PIL.Image
import PIL.ImageDraw
from os.path        import join
from urllib.request         import FancyURLopener
from os             import unlink, getenv

from .gml_generator   import GMLGenerator
from .gml_parser      import gml_import
from .gml_sd_parser    import gml_sd_import
from .gml            import GMLStructure
from .utils import utOpen, zip_generator
from .gml_image import gmlToSimpleImage
from .gml_image import gmlToBgImage
from . import gml_geometry

EXTENSIONS = ['.dbf', '.shp', '.shx']
FILES_PATH = getenv('TEMP')

#parse SHP/generate GML
def createShpToGmlFiles(shp_file, shx_file, dbf_file):
    from OFS.Image import cookId
    shp_filename, title = cookId('', '', shp_file)
    shx_filename, title = cookId('', '', shx_file)
    dbf_filename, title = cookId('', '', dbf_file)

    #temporary create files
#    fld_path = join(FILES_PATH, shp_filename[:-4])
#    if not os.path.isdir(fld_path):
#        os.mkdir(fld_path)

    shp_path = join(FILES_PATH, shp_filename)
    shp_data = shp_file.read()
    temp_shp_file = open(shp_path, 'wb')
    temp_shp_file.write(shp_data)
    temp_shp_file.close()
    
    shx_path = join(FILES_PATH, shx_filename)
    shx_data = shx_file.read()
    temp_shx_file = open(shx_path, 'wb')
    temp_shx_file.write(shx_data)
    temp_shx_file.close()
    
    dbf_path = join(FILES_PATH, dbf_filename)
    dbf_data = dbf_file.read()
    temp_dbf_file = open(dbf_path, 'wb')
    temp_dbf_file.write(dbf_data)
    temp_dbf_file.close()
    
    return shp_filename[:-4]

def deleteShpToGmlFiles(filename):
    #delete created files
    for k in EXTENSIONS:
        os.unlink(join(FILES_PATH, '%s%s' % (filename, k)))
