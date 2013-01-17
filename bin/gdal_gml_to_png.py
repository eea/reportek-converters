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
    arguments = parser.parse_args()
    with NamedTemporaryFile() as gtiff_file:
        rasterize_command_string = ('gdal_rasterize -q'
                                        ' -init 255'
                                        ' -burn 255 -burn 0 -burn 0'
                                        ' -of GTiff -ts {width} {height}'
                                        ' {src} {dst}')
        rasterize_command = rasterize_command_string.format(**{
                                'width': constants.IMAGE_WIDTH,
                                'height': constants.IMAGE_HEIGHT,
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
