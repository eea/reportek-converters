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
      Reproduces an ARCIMS XML response object structure and defines getters/setters for the elements
"""

from .utils import utf8Encode

class IMSObject:
    """ Reproduces an ARCIMS XML object structure and defines getters/setters for the elements """

    def __init__(self):
        """ constructor """
        #general
        self.__minx__=''
        self.__miny__ = ''
        self.__maxx__ = ''
        self.__maxy__ = ''
        self.__url__ = ''
        self.__ims_error__ = ''

    ##################################################
    # Generic getters/setters
    ##################################################

    def getMinx(self):
        return (self.__minx__)

    def setMinx(self,minx):
        self.__minx__ = utf8Encode(minx)

    def getMiny(self):
        return (self.__miny__)

    def setMiny(self,miny):
        self.__miny__ = utf8Encode(miny)

    def getMaxx(self):
        return (self.__maxx__)

    def setMaxx(self,maxx):
        self.__maxx__ = utf8Encode(maxx)

    def getMaxy(self):
        return (self.__maxy__)

    def setMaxy(self,maxy):
        self.__maxy__ = utf8Encode(maxy)

    def getUrl(self):
        return (self.__url__)

    def setUrl(self,url):
        self.__url__ = utf8Encode(url)

    def getIms_error(self):
        return (self.__ims_error__)

    def setIms_error(self,ims_error):
        self.__ims_error__ = utf8Encode(ims_error)