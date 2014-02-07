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
      ARC IMS response parser module
"""

from xml.sax.handler import ContentHandler
from xml.sax         import *
from cStringIO       import StringIO
from types           import StringType

from ims_object      import IMSObject

_DATA_TAGS = ['ERROR']

def ims_response_import(file):

    ims_res_val = IMSObject()
    parser = ims_res_parser()

    #parse the ins response information
    chandler = parser.parseHeader(file, ims_res_val)
    ims_res_obj = chandler.getIMSRespVal()

    #return an IMSResponse object 
    return ims_res_obj


class ims_res_handler(ContentHandler):
    """ This is used to parse the ims response xml
    """
    def __init__(self, ims_res_val):
        """ constructor """
        self.ims_res_val = ims_res_val
        self.__currentTag = ''
        self.__data = []
        self.__tagout=''

    def getIMSRespVal(self):
        return self.ims_res_val

    def startElement(self, name, attrs):
        if name == 'ENVELOPE':
            for elem in attrs.keys():
                if elem == 'minx':
                    self.ims_res_val.setMinx(attrs['minx'])
                if elem == 'miny':
                    self.ims_res_val.setMiny(attrs['miny'])
                if elem == 'maxx':
                    self.ims_res_val.setMaxx(attrs['maxx'])
                if elem == 'maxy':
                    self.ims_res_val.setMaxy(attrs['maxy'])
        if name == 'OUTPUT':
            for elem in attrs.keys():
                if elem == 'url':
                    self.ims_res_val.setUrl(attrs['url'])

        self.__currentTag = name

    def endElement(self, name):
        self.__currentTag = ''
        if name in _DATA_TAGS:
            self.ims_res_val.setIms_error(u''.join(self.__data).strip())
            print self.ims_res_val.getIms_error()
            
    def characters(self, content):
        currentTag = self.__currentTag
        if currentTag in _DATA_TAGS:
            self.__data.append(content)

class ims_res_parser:
    """ class for parse ims files """

    def __init__(self):
        """ """
        pass

    def parseContent(self, xml_string):
        """ """
        parser = make_parser()
        chandler = ims_res_handler()
        # Tell the parser to use our handler
        parser.setContentHandler(chandler)

        parser.setFeature(handler.feature_external_ges, 0)

        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO(xml_string))
        try:
            parser.parse(inpsrc)
            return chandler
        except:
            return None

    def parseHeader(self, file, ims_res_val):
        # Create a parser
        parser = make_parser()
        chandler = ims_res_handler(ims_res_val)
        # Tell the parser to use our handler
        parser.setContentHandler(chandler)

        try:
            parser.setFeature(handler.feature_external_ges, 0)
        except:
            pass
        inputsrc = InputSource()

        try:
            if type(file) is StringType:
                inputsrc.setByteStream(StringIO(file))
            else:
                filecontent = file.read()
                inputsrc.setByteStream(StringIO(filecontent))
            parser.parse(inputsrc)
            return chandler
        except:
            return None