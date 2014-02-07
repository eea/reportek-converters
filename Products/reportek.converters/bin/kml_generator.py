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
    Google Earth KML template module.
"""

from string import strip

class KMLGenerator:

    def __init__(self):
        """ constructor """
        pass

    def fillKMLHeader(self):
        kml_header = [] 
        k_a = kml_header.append
        k_a('<?xml version="1.0" encoding="UTF-8"?>')
        k_a('<kml xmlns="http://earth.google.com/kml/2.1">')
        k_a('<Document>')
        return '\n'.join(kml_header)

    def fillKMLFooter(self):
        kml_footer = []
        k_a = kml_footer.append
        k_a('</Document>')
        k_a('</kml>')
        return '\n'.join(kml_footer)

    def fillKMLStyle(self):
        kml_style = []
        k_a = kml_style.append
        k_a('<Style id="myDefaultStyles">')
        k_a('<IconStyle id="IconStyle">')
        k_a('<color>ff0000ff</color>')
        k_a('<Icon>')
        k_a('<href>root://icons/palette-4.png</href>')
        k_a('<y>128</y>')
        k_a('<w>32</w>')
        k_a('<h>32</h>')
        k_a('</Icon>')
        k_a('</IconStyle>')
        k_a('<LabelStyle id="defaultLabelStyle">')
        k_a('<color>7fffaaff</color>')
        k_a('<scale>1.5</scale>')
        k_a('</LabelStyle>')
        k_a('<LineStyle id="defaultLineStyle">')
        k_a('<color>ff0000ff</color>')
        k_a('<width>15</width>')
        k_a('</LineStyle>')
        k_a('<PolyStyle id="defaultPolyStyle">')
        k_a('<color>ff0000ff</color>')
        k_a('<fill>1</fill>')
        k_a('<outline>1</outline>')
        k_a('</PolyStyle>')
        k_a('</Style>')
        return '\n'.join(kml_style)

    def fillKMLPoint(self, name, in_long, in_lat):
        kml_placemark = []
        k_a = kml_placemark.append
        k_a('<Placemark>')
        k_a('<name>%s</name>' % name)
        k_a('<visibility>1</visibility>')
        k_a('<styleUrl>#myDefaultStyles</styleUrl>')
        k_a('<Point id="IconStyle">')
        k_a('<coordinates>%s,%s,0.0</coordinates>' % (in_long, in_lat))
        k_a('</Point>')
        k_a('</Placemark>')
        return '\n'.join(kml_placemark)

    def fillKMLLine(self, name, vertices):
        kml_line = [] 
        kl_a = kml_line.append
        kl_a('<Placemark>')
        kl_a('<name>%s</name>' % name)
        kl_a('<visibility>1</visibility>')
        kl_a('<styleUrl>#myDefaultStyles</styleUrl>')
        for k in range (len(vertices)):
            kl_a('<LineString id="defaultLineStyle">')
            kl_a('<altitudeMode>absolute</altitudeMode>')
            l_vmtoadd = ""
            for j in (vertices[k]):
                l_vmtoadd = l_vmtoadd +('%s,%s,0.0 ' % (j[0],j[1]))
            kl_a('<coordinates>%s</coordinates>' % strip(l_vmtoadd))
            kl_a('</LineString>')
        kl_a('</Placemark>')
        return '\n'.join(kml_line)

    def fillKMLPoly(self, name, vertices):
        kml_line = [] 
        kl_a = kml_line.append
        kl_a('<Placemark>')
        kl_a('<name>%s</name>' % name)
        kl_a('<visibility>1</visibility>')
        kl_a('<styleUrl>#myDefaultStyles</styleUrl>')
        for k in range (len(vertices)):
            kl_a('<Polygon id="defaultPolyStyle">')
            kl_a('<outerBoundaryIs>')
            kl_a('<LinearRing>')
            kl_a('<altitudeMode>absolute</altitudeMode>')
            l_vmtoadd = ""
            for j in (vertices[k]):
                l_vmtoadd = l_vmtoadd +('%s,%s,0.0 ' % (j[0],j[1]))
            kl_a('<coordinates>%s</coordinates>' % strip(l_vmtoadd))
            kl_a('</LinearRing>')
            kl_a('</outerBoundaryIs>')
            kl_a('</Polygon>')
        kl_a('</Placemark>')
        return '\n'.join(kml_line)