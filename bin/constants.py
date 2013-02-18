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

# draw colors
OUTLINE_RGB = 'rgb(255,0,0)'
FILL_RGB = 'rgb(255,0,0)'

# image size
IMAGE_WIDTH = 680
IMAGE_HEIGHT = 600

# image thumbnail size
IMAGE_WIDTH_TH = 320
IMAGE_HEIGHT_TH = 200

# image type
IMAGE_TYPE = 'png'

# IMS server parameters
IMS_SERVER = 'geonode-test.eea.eu.int'
IMS_SERVICE = 'gml_test_dtm'

XSD_FILE = "http://biodiversity.eionet.europa.eu/schemas/dir9243eec/gml_art17.xsd"

# temporary dictionary with bounding boxes
COUNTRIES_DICT = {'EU':{'minx': '2400000.0', 'miny':'1250000.0', \
 'maxx':'7300000.0', 'maxy':'5500000.0'}, \
 'IS':{'minx': '2770573.16189', 'miny':'4765314.89549', \
 'maxx':'3245404.59425', 'maxy':'5162182.47357'}, \
 'IE':{'minx': '2938456.76326', 'miny':'3327596.29852', \
 'maxx':'3274566.55405', 'maxy':'3718634.66667'}, \
 'GB':{'minx': '3156760.79912', 'miny':'3095105.63798', \
 'maxx':'3763366.03014', 'maxy':'4239198.38618'}, \
 'NO':{'minx': '4039280.52876', 'miny':'3879964.23311', \
 'maxx':'5131651.23749', 'maxy':'5414446.78447'}, \
 'SE':{'minx': '4385107.71231', 'miny':'3586506.87577', \
 'maxx':'4968478.32235', 'maxy':'5136240.72666'}, \
 'AD':{'minx': '3615426.60582', 'miny':'2187130.60422', \
 'maxx':'3645572.98945', 'maxy':'2211160.44977'}, \
 'MC':{'minx': '4110368.63101', 'miny':'2294594.5744', \
 'maxx':'4114324.22916', 'maxy':'2299005.21236'}, \
 'AL':{'minx': '5088829.21981', 'miny':'1898156.60444', \
 'maxx':'5256952.41312', 'maxy':'2224228.01213'}, \
 'BA':{'minx': '4775200.83273', 'miny':'2201300.84223', \
 'maxx':'5091651.80925', 'maxy':'2486706.72079'}, \
 'HR':{'minx': '4595209.44505', 'miny':'2183594.81623', \
 'maxx':'5060265.901', 'maxy':'2623559.0682'}, \
 'IT':{'minx': '4055004.72994', 'miny':'1524204.94712', \
 'maxx':'5049029.31574', 'maxy':'2667007.90472'}, \
 'MK':{'minx': '5194314.71145', 'miny':'2040385.06677', \
 'maxx':'5404182.63498', 'maxy':'2222508.55379'}, \
 'SM':{'minx': '4514618.14447', 'miny':'2313181.65812', \
 'maxx':'4523030.45382', 'maxy':'2323042.36786'}, \
 'CS':{'minx': '5004124.16594', 'miny':'2131278.82141', \
 'maxx':'5375062.68041', 'maxy':'2614703.29516'}, \
 'VC':{'minx': '4524544.75395', 'miny':'2091940.16999', \
 'maxx':'4525643.16281', 'maxy':'2092774.22964'}, \
 'BG':{'minx': '5313045.79388', 'miny':'2119471.71097', \
 'maxx':'5811196.36791', 'maxy':'2495070.90947'}, \
 'CY':{'minx': '6341979.54213', 'miny':'1595628.36376', \
 'maxx':'6525896.20855', 'maxy':'1759763.04554'}, \
 'GR':{'minx': '5149146.95225', 'miny':'1451546.25478', \
 'maxx':'5953825.68654', 'maxy':'2216076.84588'}, \
 'TR':{'minx': '5652444.46812', 'miny':'1678248.89666', \
 'maxx':'7316569.1976', 'maxy':'2644977.78114'}, \
 'AT':{'minx': '4285681.00112', 'miny':'2598946.54632', \
 'maxx':'4854986.83296', 'maxy':'2890953.82128'}, \
 'CZ':{'minx': '4470090.3176', 'miny':'2839056.73209', \
 'maxx':'4960266.22525', 'maxy':'3113470.05957'}, \
 'DK':{'minx': '4200602.16508', 'miny':'3496822.57605', \
 'maxx':'4649625.78535', 'maxy':'3849478.63775'}, \
 'HU':{'minx': '4786786.34296', 'miny':'2551466.48104', \
 'maxx':'5279046.43509', 'maxy':'2894488.26914'}, \
 'PL':{'minx': '4597984.52902', 'miny':'2945574.9321', \
 'maxx':'5313701.71851', 'maxy':'3556503.9738'}, \
 'SK':{'minx': '4827530.82686', 'miny':'2767717.91993', \
 'maxx':'5233849.49464', 'maxy':'2991270.26786'}, \
 'SI':{'minx': '4581890.39347', 'miny':'2488521.29219', \
 'maxx':'4828229.59599', 'maxy':'2660312.5506'}, \
 'BE':{'minx': '3799506.03977', 'miny':'2942892.42482', \
 'maxx':'4064600.86508', 'maxy':'3167381.47052'}, \
 'FR':{'minx': '3230940.21722', 'miny':'2029704.63031', \
 'maxx':'4284761.42087', 'maxy':'3135511.24263'}, \
 'DE':{'minx': '4031189.2323', 'miny':'2684585.02974', \
 'maxx':'4672112.77385', 'maxy':'3551252.37129'}, \
 'LI':{'minx': '4281052.48303', 'miny':'2660576.78522', \
 'maxx':'4293200.45144', 'maxy':'2684661.84573'}, \
 'LU':{'minx': '4014289.08848', 'miny':'2933915.09237', \
 'maxx':'4070867.02016', 'maxy':'3015451.24302'}, \
 'NL':{'minx': '3859677.67879', 'miny':'3079405.45807', \
 'maxx':'4134668.12752', 'maxy':'3380607.8074'}, \
 'CH':{'minx': '4009570.54377', 'miny':'2524600.0696', \
 'maxx':'4358303.86307', 'maxy':'2744719.63588'}, \
 'BY':{'minx': '5201856.46686', 'miny':'3245235.23503', \
 'maxx':'5805397.19936', 'maxy':'3816548.62921'}, \
 'EE':{'minx': '5008542.19575', 'miny':'3927496.7766', \
 'maxx':'5367317.0039', 'maxy':'4171144.28633'}, \
 'FI':{'minx': '4746036.21801', 'miny':'4138589.75225', \
 'maxx':'5402813.29861', 'maxy':'5306376.04092'}, \
 'LV':{'minx': '4993488.59107', 'miny':'3716569.31776', \
 'maxx':'5437803.12758', 'maxy':'3983390.24392'}, \
 'LT':{'minx': '5006495.53121', 'miny':'3508509.32004', \
 'maxx':'5378543.97921', 'maxy':'3800248.04299'}, \
 'MD':{'minx': '5544591.29892', 'miny':'2655580.35871', \
 'maxx':'5848834.24268', 'maxy':'2972849.78017'}, \
 'RO':{'minx': '5112288.44938', 'miny':'2390894.50699', \
 'maxx':'5853700.46783', 'maxy':'2934477.48771'}, \
 'UA':{'minx': '5213915.68579', 'miny':'2640194.52835', \
 'maxx':'6482661.40414', 'maxy':'3514448.39724'}, \
 'ES':{'minx': '2760814.91386', 'miny':'1581936.14589', \
 'maxx':'3769128.01242', 'maxy':'2466865.08218'}, \
 'PT':{'minx': '2636675.4652', 'miny':'1735185.70032', \
 'maxx':'2977222.60791', 'maxy':'2297820.00945'}, \
 'RU':{'minx': '4954602.46747', 'miny':'3523884.62892', \
 'maxx':'5147298.30932', 'maxy':'3632673.03855'}}


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
