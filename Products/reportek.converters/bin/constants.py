# -*- coding: utf8 -*-
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
      Constants and templates
"""

from os import getenv

EXTENSIONS = ['.dbf', '.shp', '.shx', '.xml', '.prj']
FILES_PATH = getenv('TMPDIR')

# image size
IMAGE_WIDTH = 680
IMAGE_HEIGHT = 600

# image thumbnail size
IMAGE_WIDTH_TH = 320
IMAGE_HEIGHT_TH = 200

XSD_FILE = "http://biodiversity.eionet.europa.eu/schemas/dir9243eec/gml_art17.xsd"


METADATA_LABELS = {'met:mapOwner':'Owner of the map', \
'met:organisationName':'Organisation name', \
'met:owncontactPerson':'Contact person', \
'met:addressDeliveryPoint':'Address (delivery point)', \
'met:addressCity':'Address (City)', \
'met:addressPostalCode':'Address (Postal code)', \
'met:addressCountry':'Address (Country)', \
'met:ownaddressEmail':'Address (email)', \
'met:ownaddressWebSite':'Address (web site)', \
'met:mapNotes':'Map notes', \
'met:title':'Title', \
'met:footnote':'Footnote', \
'met:briefAbstract':'Brief abstract', \
'met:keywords':'Keywords', \
'met:referenceDate':'Reference date', \
'met:copyrights':'Copyrights', \
'met:mapinreports':'Main reports', \
'met:maponweb':'Map on web', \
'met:methodology':'Methodology description', \
'met:desc':'Description', \
'met:datasetsRetrievedFrom':'Datasets retrieved from', \
'met:name':'Name', \
'met:organisation':'Organisation/source name', \
'met:contactPerson':'Contact person', \
'met:addressEmail':'Address (email)', \
'met:addressWebSite':'Address (web site)', \
'met:productionYear':'Production year', \
'met:url':'URL', \
'met:otherRelevantInfo':'Other relevant information'}

METADATA_TEMPLATE = """<met:mapOwner label="Owner of the map">
<met:organisationName label="Organisation name">%s</met:organisationName>
<met:owncontactPerson label="Contact person">%s</met:owncontactPerson>
<met:addressDeliveryPoint label="Address (delivery point)">%s</met:addressDeliveryPoint>
<met:addressCity label="Address (City)">%s</met:addressCity>
<met:addressPostalCode label="Address (Postal code)">%s</met:addressPostalCode>
<met:addressCountry label="Address (Country)">%s</met:addressCountry>
<met:ownaddressEmail label="Address (email)">%s</met:ownaddressEmail>
<met:ownaddressWebSite label="Address (web site)">%s</met:ownaddressWebSite>
</met:mapOwner>
<met:mapNotes label="Map notes">
<met:title label="Title">%s</met:title>
<met:footnote label="Footnote">%s</met:footnote>
<met:briefAbstract label="Brief abstract">%s</met:briefAbstract>
<met:keywords label="Keywords">%s</met:keywords>
<met:referenceDate label="Reference date">%s</met:referenceDate>
</met:mapNotes>
<met:copyrights label="Copyrights">
<met:mapinreports label="Main reports">%s</met:mapinreports>
<met:maponweb label="Map on web">%s</met:maponweb>
</met:copyrights>
<met:methodology label="Methodology description">
<met:desc label="Description">%s</met:desc>
</met:methodology>
<met:datasetsRetrievedFrom label="Datasets retrieved from">
<met:name label="Name">%s</met:name>
<met:organisation label="Organisation/source name">%s</met:organisation>
<met:contactPerson label="Contact person">%s</met:contactPerson>
<met:addressEmail label="Address (email)">%s</met:addressEmail>
<met:addressWebSite label="Address (web site)">%s</met:addressWebSite>
<met:productionYear label="Production year">%s</met:productionYear>
<met:url label="URL">%s</met:url>
<met:otherRelevantInfo label="Other relevant information">%s</met:otherRelevantInfo>
</met:datasetsRetrievedFrom>"""

PROJECTION_LABELS = {'met:projection':'ESRI projection metadata'}

PROJECTION_TEMPLATE = """<met:projection label="ESRI projection metadata">%s</met:projection>"""

PROJECTION = 'ETRS_1989_LAEA_52N_10E'
