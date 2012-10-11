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
Tempaltes for GML generation
"""

from utils  import utGMLEncode
from string import strip
from constants       import *

class GMLGenerator:

    def __init__(self, user_enc):
        self.__user_enc = user_enc

    def fillHeader(self, p_schema_loc):
        gml_header = [] 
        h_a = gml_header.append
        h_a('<?xml version="1.0" encoding="UTF-8"?>')
        h_a('<gml:FeatureCollection')
        h_a('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        h_a('xsi:noNamespaceSchemaLocation="%s"' % (p_schema_loc))
        h_a('xmlns:gml="http://www.opengis.net/gml"')
        h_a('xmlns:met="http://biodiversity.eionet.europa.eu/schemas/dir9243eec">')
        h_a('<gml:metaDataProperty>')
        return '\n'.join(gml_header)

    def fillBoundingBox(self, minX, minY, maxX, maxY):
        gml_box = [] 
        bb_a = gml_box.append
        bb_a('\n</met:info>')
        bb_a('</gml:metaDataProperty>')
        bb_a('<gml:boundedBy>')
        bb_a('<gml:Envelope>')
        bb_a('<gml:coord>')
        bb_a('<gml:X>%.8f' % minX + '</gml:X>')
        bb_a('<gml:Y>%.8f' % minY + '</gml:Y>')
        bb_a('</gml:coord>')
        bb_a('<gml:coord>')
        bb_a('<gml:X>%.8f' % maxX + '</gml:X>')
        bb_a('<gml:Y>%.8f' % maxY + '</gml:Y>')
        bb_a('</gml:coord>')
        bb_a('</gml:Envelope>')
        bb_a('</gml:boundedBy>')
        return '\n'.join(gml_box)

    def fillProjection(self, val):
        gml_prj = []
        pr_a = gml_prj.append
        pr_a(PROJECTION_TEMPLATE % utGMLEncode(val, self.__user_enc))
        return '\n'.join(gml_prj)

    def fillMetadata(self, val, filename):
        gml_meta = [] 
        fmp_a = gml_meta.append
        fmp_a('\n<met:info href="%s.gml">' % (filename))
        fmp_a(METADATA_TEMPLATE % (utGMLEncode(val['met:organisationName'], self.__user_enc), \
        utGMLEncode(val['met:owncontactPerson'], self.__user_enc), \
        utGMLEncode(val['met:addressDeliveryPoint'], self.__user_enc), \
        utGMLEncode(val['met:addressCity'], self.__user_enc), \
        utGMLEncode(val['met:addressPostalCode'], self.__user_enc), \
        utGMLEncode(val['met:addressCountry'], self.__user_enc), \
        utGMLEncode(val['met:ownaddressEmail'], self.__user_enc), \
        utGMLEncode(val['met:ownaddressWebSite'], self.__user_enc), \
        utGMLEncode(val['met:title'], self.__user_enc), \
        utGMLEncode(val['met:footnote'], self.__user_enc), \
        utGMLEncode(val['met:briefAbstract'], self.__user_enc), \
        utGMLEncode(val['met:keywords'], self.__user_enc), \
        utGMLEncode(val['met:referenceDate'], self.__user_enc), \
        utGMLEncode(val['met:mapinreports'], self.__user_enc), \
        utGMLEncode(val['met:maponweb'], self.__user_enc), \
        utGMLEncode(val['met:desc'], self.__user_enc), \
        utGMLEncode(val['met:name'], self.__user_enc), \
        utGMLEncode(val['met:organisation'], self.__user_enc), \
        utGMLEncode(val['met:contactPerson'], self.__user_enc), \
        utGMLEncode(val['met:addressEmail'], self.__user_enc), \
        utGMLEncode(val['met:addressWebSite'], self.__user_enc), \
        utGMLEncode(val['met:productionYear'], self.__user_enc), \
        utGMLEncode(val['met:url'], self.__user_enc), \
        utGMLEncode(val['met:otherRelevantInfo'], self.__user_enc)))
        return '\n'.join(gml_meta)

    def fillExportMetadata(self, val, filename):
        gml_meta = [] 
        fmp_a = gml_meta.append
        fmp_a('<?xml version="1.0" encoding="UTF-8"?>')
        fmp_a('<met:info xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
        fmp_a('xmlns:met="http://biodiversity.eionet.europa.eu/schemas/dir9243eec"')
        fmp_a('xsi:schemaLocation="http://biodiversity.eionet.europa.eu/schemas/dir9243eec http://biodiversity.eionet.europa.eu/schemas/dir9243eec/gml_art17_meta.xsd" href="%s.gml">' % (filename))
        fmp_a(METADATA_TEMPLATE % (utGMLEncode(val['met:organisationName'], self.__user_enc), \
        utGMLEncode(val['met:owncontactPerson'], self.__user_enc), \
        utGMLEncode(val['met:addressDeliveryPoint'], self.__user_enc), \
        utGMLEncode(val['met:addressCity'], self.__user_enc), \
        utGMLEncode(val['met:addressPostalCode'], self.__user_enc), \
        utGMLEncode(val['met:addressCountry'], self.__user_enc), \
        utGMLEncode(val['met:ownaddressEmail'], self.__user_enc), \
        utGMLEncode(val['met:ownaddressWebSite'], self.__user_enc), \
        utGMLEncode(val['met:title'], self.__user_enc), \
        utGMLEncode(val['met:footnote'], self.__user_enc), \
        utGMLEncode(val['met:briefAbstract'], self.__user_enc), \
        utGMLEncode(val['met:keywords'], self.__user_enc), \
        utGMLEncode(val['met:referenceDate'], self.__user_enc), \
        utGMLEncode(val['met:mapinreports'], self.__user_enc), \
        utGMLEncode(val['met:maponweb'], self.__user_enc), \
        utGMLEncode(val['met:desc'], self.__user_enc), \
        utGMLEncode(val['met:name'], self.__user_enc), \
        utGMLEncode(val['met:organisation'], self.__user_enc), \
        utGMLEncode(val['met:contactPerson'], self.__user_enc), \
        utGMLEncode(val['met:addressEmail'], self.__user_enc), \
        utGMLEncode(val['met:addressWebSite'], self.__user_enc), \
        utGMLEncode(val['met:productionYear'], self.__user_enc), \
        utGMLEncode(val['met:url'], self.__user_enc), \
        utGMLEncode(val['met:otherRelevantInfo'], self.__user_enc)))
        fmp_a('</met:info>')
        return '\n'.join(gml_meta)

    def fillFeatureMemberPoint(self, fID, X, Y, dbfValues):
        gml_point = [] 
        fmp_a = gml_point.append
        fmp_a('\n<gml:featureMember>')
        fmp_a('<reportnet fid="%s">' % fID)
        fmp_a('<geometryProperty>')
        fmp_a('<gml:Point>')
        fmp_a('<gml:coordinates>%s,%s</gml:coordinates>' % (X,Y))
        fmp_a('</gml:Point>')
        fmp_a('</geometryProperty>')
        for k,v in (dbfValues.items()):
            fmp_a('<%s>%s</%s>' % (utGMLEncode(k, self.__user_enc), utGMLEncode(v, self.__user_enc), utGMLEncode(k, self.__user_enc)))
        fmp_a('</reportnet>')
        fmp_a('</gml:featureMember>')
        return '\n'.join(gml_point)

    def fillFeatureMemberLine(self, fID, vertices, dbfValues):
        gml_point = [] 
        fml_a = gml_point.append
        fml_a('\n<gml:featureMember>')
        fml_a('<reportnet fid="%s">' % fID)
        fml_a('<geometryProperty>')
        if len(vertices) == 1:
            fml_a('<gml:LineString>')
            l_vtoadd = ""
            for k in range (len(vertices)):
                for j in (vertices[k]):
                    l_vtoadd = l_vtoadd + ('%s,%s ' % (j[0],j[1]))
            fml_a('<gml:coordinates>%s</gml:coordinates>' % strip(l_vtoadd))
            fml_a('</gml:LineString>')
        elif len(vertices) > 1:
            fml_a('<gml:MultiLineString>')
            for k in range (len(vertices)):
                fml_a('<gml:lineStringMember>')
                fml_a('<gml:LineString>')
                l_vmtoadd = ""
                for j in (vertices[k]):
                    l_vmtoadd = l_vmtoadd +('%s,%s ' % (j[0],j[1]))
                fml_a('<gml:coordinates>%s</gml:coordinates>' % strip(l_vmtoadd))
                fml_a('</gml:LineString>')
                fml_a('</gml:lineStringMember>')
            fml_a('</gml:MultiLineString>')
        fml_a('</geometryProperty>')
        for k,v in (dbfValues.items()):
            fml_a('<%s>%s</%s>' % (utGMLEncode(k, self.__user_enc), utGMLEncode(v, self.__user_enc), utGMLEncode(k, self.__user_enc)))
        fml_a('</reportnet>')
        fml_a('</gml:featureMember>')
        return '\n'.join(gml_point)

    def fillFeatureMemberPolygon(self, fID, vertices, dbfValues):
        gml_polygon = [] 
        fmpl_a = gml_polygon.append
        fmpl_a('\n<gml:featureMember>')
        fmpl_a('<reportnet fid="%s">' % fID)
        fmpl_a('<geometryProperty>')
        if len(vertices) == 1:
            fmpl_a('<gml:Polygon>')
            fmpl_a('<gml:outerBoundaryIs>')
            fmpl_a('<gml:LinearRing>')
            l_vtoadd = ""
            for vert in vertices[0]:
                l_vtoadd = l_vtoadd+ ('%s,%s ' % (vert[0], vert[1]))
            fmpl_a('<gml:coordinates>%s</gml:coordinates>' % strip(l_vtoadd))
            fmpl_a('</gml:LinearRing>')
            fmpl_a('</gml:outerBoundaryIs>')
            fmpl_a('</gml:Polygon>')
        elif len(vertices) > 1:
            fmpl_a('<gml:MultiPolygon>')
            for k in range (len(vertices)):
                fmpl_a('<gml:polygonMember>')
                fmpl_a('<gml:Polygon>')
                fmpl_a('<gml:outerBoundaryIs>')
                fmpl_a('<gml:LinearRing>')
                l_vmtoadd = ""
                for j in (vertices[k]):
                    l_vmtoadd = l_vmtoadd +('%s,%s ' % (j[0],j[1]))
                fmpl_a('<gml:coordinates>%s</gml:coordinates>' % strip(l_vmtoadd))
                fmpl_a('</gml:LinearRing>')
                fmpl_a('</gml:outerBoundaryIs>')
                fmpl_a('</gml:Polygon>')
                fmpl_a('</gml:polygonMember>')                    
            fmpl_a('</gml:MultiPolygon>')                
        fmpl_a('</geometryProperty>')
        for k,v in (dbfValues.items()):
            fmpl_a('<%s>%s</%s>' % (utGMLEncode(k, self.__user_enc), utGMLEncode(v, self.__user_enc), utGMLEncode(k, self.__user_enc)))
        fmpl_a('</reportnet>')
        fmpl_a('</gml:featureMember>')
        return '\n'.join(gml_polygon)

    def fillFooter(self):
        gml_footer = []
        f_a = gml_footer.append
        f_a('\n</gml:FeatureCollection>')
        return '\n'.join(gml_footer)

    def fillSDHeader(self):
        gml_sd_header = [] 
        h_a = gml_sd_header.append
        h_a('<?xml version="1.0" encoding="UTF-8"?>')
        h_a('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"')
        h_a('xmlns:gml="http://www.opengis.net/gml"')
        h_a('elementFormDefault="qualified" version="3.1.1">')

        h_a('<xs:import namespace="http://www.opengis.net/gml" schemaLocation="http://schemas.opengis.net/gml/3.1.1/base/feature.xsd"/>')
        h_a('<xs:import namespace="http://www.opengis.net/gml" schemaLocation="http://schemas.opengis.net/gml/3.1.1/base/geometryBasic0d1d.xsd"/>')

        h_a('<xs:element name="FeatureCollection" type="gml:FeatureCollectionType" substitutionGroup="gml:_FeatureCollection"/>')
        h_a('<xs:complexType name="FeatureCollectionType">')
        h_a('<xs:complexContent>')
        h_a('<xs:extension base="gml:AbstractFeatureCollectionType">')
        h_a('<xs:attribute name="lockId" type="xs:string" use="optional"/>')
        h_a('<xs:attribute name="scope" type="xs:string" use="optional"/>')
        h_a('</xs:extension>')
        h_a('</xs:complexContent>')
        h_a('</xs:complexType>')

        h_a('<xs:element name="_MetaData" type="gml:AbstractMetaDataType" abstract="true" substitutionGroup="gml:_Object">/')

        h_a('<xs:complexType name="AbstractMetaDataType" abstract="true" mixed="true">')
        h_a('<xs:attribute ref="gml:id" use="optional" /> ')
        h_a('</xs:complexType>')

        h_a('<xs:element name="metaDataProperty" substitutionGroup="gml:_MetaData">')
        h_a('<xs:complexType>')
        h_a('<xs:complexContent mixed="true" >')
        h_a('<xs:extension base="gml:AbstractMetaDataType">')
        h_a('<xs:sequence>')
        h_a('<xs:element name="datasetName" minOccurs="0" nillable="true" type="xs:string"/>')
        h_a('</xs:sequence>')
        h_a('</xs:extension>')
        h_a('</xs:complexContent>')
        h_a('</xs:complexType>')
        h_a('</xs:element>')




        h_a('<xs:element name="reportnet" substitutionGroup="gml:_Feature">')
        h_a('<xs:complexType>')
        h_a('<xs:complexContent>')
        h_a('<xs:extension base="gml:AbstractFeatureType">')
        h_a('<xs:choice maxOccurs="unbounded">')
        h_a('<xs:element name="geometryProperty" type="gml:GeometryPropertyType" nillable="true" minOccurs="1" maxOccurs="1"/>')
        return '\n'.join(gml_sd_header)

    def fillFeatureSD(self, dbfDef):
        gml_sd = [] 
        fsd = gml_sd.append
        for i in range(dbfDef.field_count()):
            type, name, len, decc = dbfDef.field_info(i)
            #TODO :- add dbflibc.FTInvalid
            if type == 0: #dbflibc.FTString
                fsd('<xs:element name="%s" nillable="true" minOccurs="0" maxOccurs="1">' % name)
                fsd('<xs:simpleType>')
                fsd('<xs:restriction base="xs:string">')
                fsd('<xs:maxLength value="%s"/>' % len)
                fsd('</xs:restriction>')
                fsd('</xs:simpleType>')
                fsd('</xs:element>')
            elif type == 1: #dbflibc.FTInteger
                fsd('<xs:element name="%s" nillable="true" minOccurs="0" maxOccurs="1">'% name)
                fsd('<xs:simpleType>')
                fsd('<xs:restriction base="xs:integer">')
                fsd('<xs:totalDigits value="%s"/>' % len)
                fsd('</xs:restriction>')
                fsd('</xs:simpleType>')
                fsd('</xs:element>')
            elif type == 2: #dbflibc.FTDouble
                fsd('<xs:element name="%s" nillable="true" minOccurs="0" maxOccurs="1">'% name)
                fsd('<xs:simpleType>')
                fsd('<xs:restriction base="xs:decimal">')
                fsd('<xs:totalDigits value="%s"/>' % len)
                fsd('<xs:fractionDigits value="%s"/>' % decc) 
                fsd('</xs:restriction>')
                fsd('</xs:simpleType>')
                fsd('</xs:element>') 
        return '\n'.join(gml_sd)

    def fillSDFooter(self):
        gml_sd_footer = [] 
        f_a = gml_sd_footer.append
        f_a('</xs:choice>')
        f_a('<xs:attribute name="fid" type="xs:string"/>')
        f_a('</xs:extension>')
        f_a('</xs:complexContent>')
        f_a('</xs:complexType>')
        f_a('</xs:element>')
        f_a('</xs:schema>')
        return '\n'.join(gml_sd_footer)
