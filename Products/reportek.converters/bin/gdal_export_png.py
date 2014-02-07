#!/usr/bin/env python

import subprocess
import argparse
import shlex
import sys
import os

from tempfile import NamedTemporaryFile
from path import path

import constants

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Convert maps to png.')
    parser.add_argument(
        'src_file',
        metavar='src-file',
        help='path to gml file')
    parser.add_argument(
        '--shx',
        required=False,
        default=None,
        metavar='sxh-file',
        help='path to shx file')
    parser.add_argument(
        '--dbf',
        nargs=1,
        required=False,
        default=None,
        metavar='dbf-file',
        help='path to dbf file')
    parser.add_argument(
        '-t',
        '--thumb',
        help='generate thumbnail only',
        action="store_true")
    arguments = parser.parse_args()
    with NamedTemporaryFile() as gtiff_file:
        selected_width = constants.IMAGE_WIDTH
        selected_height = constants.IMAGE_HEIGHT
        if arguments.thumb:
            selected_width = constants.IMAGE_WIDTH_TH
            selected_height = constants.IMAGE_HEIGHT_TH
        if arguments.shx:
            tmp_dir = os.environ.get('TMPDIR', '.')
            shp_path = (path(tmp_dir) / 'file.shp')
            with shp_path.open('wb') as shp_file:
                shp_file.write(path(arguments.src_file).open('rb').read())

            shx_path = (path(tmp_dir) / 'file.shx')
            with shx_path.open('wb') as shx_file:
                shx_file.write(path(arguments.shx).open('rb').read())

            rasterize_command_string = ('gdal_rasterize -q -l {layer}'
                                            ' -init 255'
                                            ' -burn 255 -burn 0 -burn 0'
                                            ' -of GTiff -ts {width} {height}'
                                            ' {src} {dst}')
            format_params = { 'width': selected_width,
                              'height': selected_height,
                              'layer': shp_path.namebase,
                              'src': shp_path,
                              'dst': gtiff_file.name }
        else:
            rasterize_command_string = ('gdal_rasterize -q'
                                            ' -init 255'
                                            ' -burn 255 -burn 0 -burn 0'
                                            ' -of GTiff -ts {width} {height}'
                                            ' {src} {dst}')
            format_params = { 'width': selected_width,
                              'height': selected_height,
                              'src': arguments.src_file,
                              'dst': gtiff_file.name }


        rasterize_command = rasterize_command_string.format(**format_params)
        subprocess.check_call(shlex.split(rasterize_command))
        try:
            #try to remove .gfs file created by gdal_rasterize in /tmp
            os.remove(arguments.src_file + '.gfs')
        except OSError:
            pass

        with NamedTemporaryFile(mode='w+') as png_file:
            translate_command_string = ('gdal_translate -q -ot Byte'
                                        ' -of PNG {0} {1}')
            translate_command = translate_command_string.format(
                                    gtiff_file.name,
                                    png_file.name)
            subprocess.check_call(shlex.split(translate_command))
            sys.stdout.write(png_file.read())
