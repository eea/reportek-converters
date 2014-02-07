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
    GML to image converter
"""
import string
import StringIO
import sys
import os
import httplib

from gml_parser     import gml_import
from gml            import GMLStructure
from ims_parser     import ims_response_import
from ims_object     import IMSObject

from constants      import *
from gml_geometry   import *
from utils          import utOpen
from os.path        import join
from urllib         import FancyURLopener
from os             import unlink
from PIL            import Image, ImageDraw, ImageFont, ImagePalette

# convert gml to image (JPEG, TIFF, PNG)
def gml_to_image(in_name, in_gml, in_width, in_height, in_filetype, in_out_colour, in_fill_colour, in_country, in_ims_server, in_ims_service, im_background = 0):

    if im_background:
        if str(in_country).upper() not in COUNTRIES_DICT:
            in_country = 'EU'
        in_country = str(in_country).upper()
        imsresp = get_background_image(in_ims_server, in_ims_service, COUNTRIES_DICT[in_country]['minx'], COUNTRIES_DICT[in_country]['miny'], COUNTRIES_DICT[in_country]['maxx'], COUNTRIES_DICT[in_country]['maxy'], in_width, in_height)

        imsresp = download_ims_image(imsresp)
        imb = Image.open (imsresp.getUrl())
        #imb = imb.convert("P")
        #imb.palette = ImagePalette.ImagePalette("RGB")

        # make a new empty image
        im = Image.new("P", (in_width, in_height),255)
        im.palette = ImagePalette.ImagePalette("RGB")
    else:
        # make a new empty image
        im = Image.new("P", (in_width, in_height),255)
        im.palette = ImagePalette.ImagePalette("RGB")

    input_gml = utOpen(in_gml)
    conv_gml = GMLStructure()
    conv_gml.setGeo_name(in_name)

    # fill geometry
    conv_gml = gml_import(input_gml.read(),conv_gml)

    # if no geographic data available
    if len(conv_gml.getShp_records()) == 0:
        #font = ImageFont.truetype("arial.ttf", 15)
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(im)
        draw.text((10, 10), " NO DATA", font=font, fill = in_out_colour)
        del draw

    if conv_gml.getFeat_type() == '1':
        for m in range(len(conv_gml.getShp_records())):
            for n in range (len(conv_gml.getShp_records()[m])):
                draw = ImageDraw.Draw(im)
                if im_background:
                    x,y = utMapToPoint((conv_gml.getShp_records()[m][n])[0][0],(conv_gml.getShp_records()[m][n])[0][1], in_width, in_height,imsresp.getMinx(),imsresp.getMiny(),imsresp.getMaxx(),imsresp.getMaxy())
                else:
                    x,y = utMapToPoint((conv_gml.getShp_records()[m][n])[0][0],(conv_gml.getShp_records()[m][n])[0][1], in_width, in_height,(conv_gml.getXY_min())[0], (conv_gml.getXY_min())[1], (conv_gml.getXY_max())[0], (conv_gml.getXY_max())[1])
                draw.rectangle([x-1,y+1,x+1,y-1], outline = in_out_colour)
                del draw
    elif conv_gml.getFeat_type() == '3':
        for m in range(len(conv_gml.getShp_records())):
            for k in range (len(conv_gml.getShp_records()[m])):
                mylist = []
                temp_mylist = mylist.append 
                for j in ((conv_gml.getShp_records()[m])[k]):
                    if im_background:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height, imsresp.getMinx(),imsresp.getMiny(),imsresp.getMaxx(),imsresp.getMaxy()))
                    else:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height,(conv_gml.getXY_min())[0], (conv_gml.getXY_min())[1], (conv_gml.getXY_max())[0], (conv_gml.getXY_max())[1]))
                draw = ImageDraw.Draw(im)
                draw.line(mylist, width = 1, fill = in_out_colour)
                del draw
    elif conv_gml.getFeat_type() == '5':
        for m in range(len(conv_gml.getShp_records())):
            #prepare polygons
            ordered_shapes = []
            temp_ordered_shapes = ordered_shapes.append
            mypoint = {}
            pol_has_poi = {}
            poi_has_pol = {}
            for k in range (len(conv_gml.getShp_records()[m])):
                t = (conv_gml.getShp_records()[m])[k][0]
                mypoint[k] = t
            for p in range(len(mypoint)):
                p_count = 0
                for k in range (len(conv_gml.getShp_records()[m])):
                    if point_inside_polygon(mypoint[p][0],mypoint[p][1],(conv_gml.getShp_records()[m])[k]) and k <>p:
                        p_count += 1
                poi_has_pol[p] = p_count
            for k in range (len(conv_gml.getShp_records()[m])):
                p_count = 0
                for p in range(len(mypoint)):
                    if point_inside_polygon(mypoint[p][0],mypoint[p][1],(conv_gml.getShp_records()[m])[k]) and k <>p:
                        p_count+=1
                pol_has_poi[k] = p_count
            pol_sort = {}
            auxlist = [ (value, key) for key, value in pol_has_poi.items() ]
            auxlist.sort()
            auxlist.reverse()
            i = 0
            for value, key in auxlist:
                pol_sort[i] = key
                i+=1

            for k in range (len(conv_gml.getShp_records()[m])):
                mylist = []
                temp_mylist = mylist.append 
                for j in ((conv_gml.getShp_records()[m])[pol_sort[k]]):
                    if im_background:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height, imsresp.getMinx(),imsresp.getMiny(),imsresp.getMaxx(),imsresp.getMaxy()))
                    else:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height,(conv_gml.getXY_min())[0], (conv_gml.getXY_min())[1], (conv_gml.getXY_max())[0], (conv_gml.getXY_max())[1]))
                draw = ImageDraw.Draw(im)
                if poi_has_pol[pol_sort[k]] % 2 == 0:
                    draw.polygon(mylist, outline = in_out_colour, fill = in_fill_colour)
                else:
                    draw.polygon(mylist, outline = in_out_colour, fill = 255)
                del draw

    if im_background:
        # cleanup
        delete_ims_image(imsresp.getUrl())


    # save the image
    file_extension = in_filetype.lower()
    if in_filetype.lower() == "jpeg":
        file_extension = "jpg"
    elif in_filetype.lower() == "TIFF":
        file_extension = "tif"
    image_url = join(FILES_PATH, "%s.%s" % (in_name, file_extension))
    if im_background:
        im.save(image_url, "%s" % in_filetype, transparency = 255, color=255)
        im = Image.open (image_url)
        im = im.convert("RGBA")
        imb = imb.convert("RGBA")
        mask = im.point(lambda i: i > 0 and 200) # use black as transparent
        imb.paste (im, (0,0), mask)
        imb.save(image_url, "%s" % in_filetype)
    else:
        im.save(image_url, "%s" % in_filetype)

    l_file = open(image_url, mode='rb')
    content = l_file.read()
    l_file.close()

    delete_ims_image(image_url)
    return content


# convert gml to image zoom (JPEG, TIFF, PNG)
def flash_ext_print(in_name, in_gml, in_width, in_height, in_filetype, in_out_colour, in_fill_colour, minx, miny, maxx, maxy, in_ims_server, in_ims_service, im_background = 0):

    if im_background:
        imsresp = get_background_image(in_ims_server, in_ims_service, minx, miny, maxx, maxy, in_width, in_height)

        imsresp = download_ims_image(imsresp)
        imb = Image.open (imsresp.getUrl())
        #imb = imb.convert("P")
        #imb.palette = ImagePalette.ImagePalette("RGB")

        # make a new empty image
        im = Image.new("P", (in_width, in_height),255)
        im.palette = ImagePalette.ImagePalette("RGB")
    else:
        # make a new empty image
        im = Image.new("P", (in_width, in_height),255)
        im.palette = ImagePalette.ImagePalette("RGB")

    input_gml = utOpen(in_gml)
    conv_gml = GMLStructure()
    conv_gml.setGeo_name(in_name)

    # fill geometry
    conv_gml = gml_import(input_gml.read(),conv_gml)

    # if no geographic data available
    if len(conv_gml.getShp_records()) == 0:
        #font = ImageFont.truetype("arial.ttf", 15)
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(im)
        draw.text((10, 10), " NO DATA", font=font, fill = in_out_colour)
        del draw

    if conv_gml.getFeat_type() == '1':
        for m in range(len(conv_gml.getShp_records())):
            for n in range (len(conv_gml.getShp_records()[m])):
                draw = ImageDraw.Draw(im)
                if im_background:
                    x,y = utMapToPoint((conv_gml.getShp_records()[m][n])[0][0],(conv_gml.getShp_records()[m][n])[0][1], in_width, in_height,imsresp.getMinx(),imsresp.getMiny(),imsresp.getMaxx(),imsresp.getMaxy())
                else:
                    x,y = utMapToPoint((conv_gml.getShp_records()[m][n])[0][0],(conv_gml.getShp_records()[m][n])[0][1], in_width, in_height,(conv_gml.getXY_min())[0], (conv_gml.getXY_min())[1], (conv_gml.getXY_max())[0], (conv_gml.getXY_max())[1])
                draw.rectangle([x-1,y+1,x+1,y-1], outline = in_out_colour)
                del draw
    elif conv_gml.getFeat_type() == '3':
        for m in range(len(conv_gml.getShp_records())):
            for k in range (len(conv_gml.getShp_records()[m])):
                mylist = []
                temp_mylist = mylist.append 
                for j in ((conv_gml.getShp_records()[m])[k]):
                    if im_background:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height, imsresp.getMinx(),imsresp.getMiny(),imsresp.getMaxx(),imsresp.getMaxy()))
                    else:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height,(conv_gml.getXY_min())[0], (conv_gml.getXY_min())[1], (conv_gml.getXY_max())[0], (conv_gml.getXY_max())[1]))
                draw = ImageDraw.Draw(im)
                draw.line(mylist, width = 1, fill = in_out_colour)
                del draw
    elif conv_gml.getFeat_type() == '5':
        for m in range(len(conv_gml.getShp_records())):
            #prepare polygons
            ordered_shapes = []
            temp_ordered_shapes = ordered_shapes.append
            mypoint = {}
            pol_has_poi = {}
            poi_has_pol = {}
            for k in range (len(conv_gml.getShp_records()[m])):
                t = (conv_gml.getShp_records()[m])[k][0]
                mypoint[k] = t
            for p in range(len(mypoint)):
                p_count = 0
                for k in range (len(conv_gml.getShp_records()[m])):
                    if point_inside_polygon(mypoint[p][0],mypoint[p][1],(conv_gml.getShp_records()[m])[k]) and k <>p:
                        p_count += 1
                poi_has_pol[p] = p_count
            for k in range (len(conv_gml.getShp_records()[m])):
                p_count = 0
                for p in range(len(mypoint)):
                    if point_inside_polygon(mypoint[p][0],mypoint[p][1],(conv_gml.getShp_records()[m])[k]) and k <>p:
                        p_count+=1
                pol_has_poi[k] = p_count
            pol_sort = {}
            auxlist = [ (value, key) for key, value in pol_has_poi.items() ]
            auxlist.sort()
            auxlist.reverse()
            i = 0
            for value, key in auxlist:
                pol_sort[i] = key
                i+=1

            for k in range (len(conv_gml.getShp_records()[m])):
                mylist = []
                temp_mylist = mylist.append 
                for j in ((conv_gml.getShp_records()[m])[pol_sort[k]]):
                    if im_background:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height, imsresp.getMinx(),imsresp.getMiny(),imsresp.getMaxx(),imsresp.getMaxy()))
                    else:
                        temp_mylist(utMapToPoint(j[0],j[1], in_width, in_height,(conv_gml.getXY_min())[0], (conv_gml.getXY_min())[1], (conv_gml.getXY_max())[0], (conv_gml.getXY_max())[1]))
                draw = ImageDraw.Draw(im)
                if poi_has_pol[pol_sort[k]] % 2 == 0:
                    draw.polygon(mylist, outline = in_out_colour, fill = in_fill_colour)
                else:
                    draw.polygon(mylist, outline = in_out_colour, fill = 255)
                del draw

    if im_background:
        # cleanup
        delete_ims_image(imsresp.getUrl())


    # save the image
    file_extension = in_filetype.lower()
    if in_filetype.lower() == "jpeg":
        file_extension = "jpg"
    elif in_filetype.lower() == "TIFF":
        file_extension = "tif"
    image_url = join(FILES_PATH, "%s.%s" % (in_name, file_extension))
    if im_background:
        im.save(image_url, "%s" % in_filetype, transparency = 255, color=255)
        im = Image.open (image_url)
        im = im.convert("RGBA")
        imb = imb.convert("RGBA")
        mask = im.point(lambda i: i > 0 and 200) # use black as transparent
        imb.paste (im, (0,0), mask)
        imb.save(image_url, "%s" % in_filetype)
    else:
        im.save(image_url, "%s" % in_filetype)

    l_file = open(image_url, mode='rb')
    content = l_file.read()
    l_file.close()

    delete_ims_image(image_url)
    return content


# get background image
def get_background_image(ims_server, ims_service, minx, miny, maxx, maxy, width, height):
    # post xml soap message
    SM_TEMPLATE = """<?xml version="1.0"?>
    <ARCXML version="1.1">
    <REQUEST>
    <GET_IMAGE>
    <PROPERTIES>
    <ENVELOPE minx="%s" miny="%s" maxx="%s" maxy="%s" />
    <IMAGESIZE width="%s" height="%s" />
    <LAYERLIST>
    <LAYERDEF id="0" visible="true" />
    <LAYERDEF id="1" visible="true" />
    <LAYERDEF id="2" visible="false" />
    <LAYERDEF id="3" visible="false" />
    <LAYERDEF id="4" visible="true" />
    </LAYERLIST>
    </PROPERTIES>
    </GET_IMAGE>
    </REQUEST>
    </ARCXML>
    """
    SoapMessage = SM_TEMPLATE % (minx, miny, maxx, maxy, width, height)

    # construct and send the header
    webservice = httplib.HTTP(ims_server)
    webservice.putrequest("POST", "/servlet/com.esri.esrimap.Esrimap?ServiceName=%s" % ims_service)
    webservice.putheader("Host", ims_server)
    webservice.putheader("User-Agent", "Python post")
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.putheader("Content-length", "%d" % len(SoapMessage))
    webservice.putheader("SOAPAction", "\"\"")
    webservice.endheaders()
    webservice.send(SoapMessage)

    # get the response
    statuscode, statusmessage, header = webservice.getreply()
    res = webservice.getfile().read()
    return ims_response_import(res)

# download the image in temp folder
def download_ims_image(imsresp):
    inputfilepath = imsresp.getUrl()
    is_via_http = 0
    if 'http' in inputfilepath:
        opener = FancyURLopener()
        is_via_http = 1
        l_file = inputfilepath
        l_filename = l_file.split('/')[-1]
        l_data = opener.open(l_file).read()
        l_file = open(join(FILES_PATH, l_filename), 'wb')
        l_file.write(l_data)
        l_file.close()
        l_temploc = inputfilepath.split('/')[-1]
        inputfilepath = join(FILES_PATH, l_temploc)
    imsresp.setUrl(inputfilepath)
    return imsresp

# delete downloaded image
def delete_ims_image(file_url):
    #delete created files
    os.unlink(file_url)

# converte coordinates in pixels
def utMapToPoint(vx, vy, w, h, minx, miny, maxx, maxy):
    # buffer for unique point geometry or overlaping (coincident) multiple points in meters (1500 km)
    if (float(maxx) == float(minx)):
        maxx = float(maxx) + float(1500000.0)
        minx = float(minx) - float(1500000.0)

    if (float(maxy) == float(miny)):
        maxy = float(maxy) + float(1500000.0)
        miny = float(miny) - float(1500000.0)

    x = vx - float(minx)
    y = float(maxy) - vy

    map_xperpixcel = w / (float(maxx) - float(minx))
    map_yperpixcel = h / (float(maxy) - float(miny))

    point_x = x * map_xperpixcel
    point_y = y * map_yperpixcel

    return point_x,point_y
