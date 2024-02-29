# -*- coding: latin1 -*-
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
    GML metadata parser INFO.
"""


from xml.sax.handler import ContentHandler
from xml.sax         import *
from io       import StringIO
from types           import StringType
from .constants       import *

def meta_import(file):
    """ """

    parser = meta_parser()
    chandler = parser.parseHeader(file)

    retMetaDict = chandler.getMetaData()
    for k in METADATA_LABELS:
        if not k in retMetaDict:
            retMetaDict[k] = ''
    return retMetaDict

class meta_handler(ContentHandler):
    """ This is used to parse the GML files
    """

    def __init__(self):
        """ constructor """
        self.__currentTag = ''
        self.__data = []
        self.__retMetaDict = {}

    def getMetaData(self):
        return self.__retMetaDict

    def startElement(self, name, attrs):
        self.__currentTag = name

    def endElement(self, name):

        if name in METADATA_LABELS:
            self.__retMetaDict[(''.join(name).strip())] = ''.join(self.__data).strip()

        if name in PROJECTION_LABELS:
            self.__retMetaDict[(''.join(name).strip())] = ''.join(self.__data).strip()


        self.__data = []
        self.__currentTag = ''


    def characters(self, content):
        currentTag = self.__currentTag
        if currentTag in METADATA_LABELS:
            self.__data.append(content)



class meta_parser:
    """ class for parse GML Metadata files """

    def __init__(self):
        """ """
        pass

    def parseContent(self, xml_string):
        """ """
        parser = make_parser()
        chandler = meta_handler()

        parser.setContentHandler(chandler)
        parser.setFeature(handler.feature_external_ges, 0)

        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO(xml_string))
        try:
            parser.parse(inpsrc)
            return chandler
        except:
            return None

    def parseHeader(self, file):
        # Create a parser
        parser = make_parser()
        chandler = meta_handler()
        # Tell the parser to use our handler
        parser.setContentHandler(chandler)
        try:
            parser.setFeature(handler.feature_external_ges, 0)
        except:
            pass
        inputsrc = InputSource()
        
        if type(file) is StringType:
            inputsrc.setByteStream(StringIO(file))
        else:
            filecontent = file.readline()
            inputsrc.setByteStream(StringIO(filecontent))
        parser.parse(inputsrc)
        return chandler
        
        try:
            if type(file) is StringType:
                inputsrc.setByteStream(StringIO(file))
            else:
                filecontent = file.readline()
                inputsrc.setByteStream(StringIO(filecontent))
            parser.parse(inputsrc)
            return chandler
        except:
            return None    
