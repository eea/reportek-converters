#!/usr/bin/env python

import subprocess
import argparse
import sys

from tempfile import NamedTemporaryFile

import constants

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Convert gml file to png.')
    parser.add_argument(
        'src_file',
        metavar='src-file',
        help='path to gml file')
    parser.add_argument(
        '-t',
        '--thumb',
        help='generate thumbnail only',
        action="store_true")
    arguments = parser.parse_args()
    with NamedTemporaryFile() as gtiff_file:
        rasterize_command_string = ('gdal_rasterize -q'
                                        ' -init 255'
                                        ' -burn 255 -burn 0 -burn 0'
                                        ' -of GTiff -ts {width} {height}'
                                        ' {src} {dst}')
        selected_width = constants.IMAGE_WIDTH
        selected_height = constants.IMAGE_HEIGHT
        if arguments.thumb:
            selected_width = constants.IMAGE_WIDTH_TH
            selected_height = constants.IMAGE_HEIGHT_TH
        rasterize_command = rasterize_command_string.format(**{
                                'width': selected_width,
                                'height': selected_height,
                                'src': arguments.src_file,
                                'dst': gtiff_file.name})
        subprocess.call(
                rasterize_command,
                shell=True)
        with NamedTemporaryFile(mode='w+') as png_file:
            translate_command_string = ('gdal_translate -q -ot Byte'
                                        ' -of PNG {0} {1}')
            translate_command = translate_command_string.format(
                                    gtiff_file.name,
                                    png_file.name)
            subprocess.call(
                    translate_command,
                    shell=True)
            sys.stdout.write(png_file.read())
