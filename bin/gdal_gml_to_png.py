#!/usr/bin/env python

import subprocess
import argparse
import sys
import os

from tempfile import NamedTemporaryFile

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Convert gml file to png.')
    parser.add_argument(
        'src_file',
        metavar='src-file',
        help='path to gml file')
    arguments = parser.parse_args()
    with open(os.devnull, 'w') as fnull:
        with NamedTemporaryFile() as gtiff_file:
            rasterize_command_string = ('gdal_rasterize'
                                            ' -burn 255 -burn 0 -burn 0'
                                            ' -of GTiff -ts 100 100 {0} {1}')
            rasterize_command = rasterize_command_string.format(
                                    arguments.src_file,
                                    gtiff_file.name)
            subprocess.call(
                    rasterize_command,
                    stdout=fnull,
                    stderr=fnull,
                    shell=True)
            with NamedTemporaryFile(mode='w+') as png_file:
                translate_command_string = ('gdal_translate'
                                            ' -of PNG {0} {1}')
                translate_command = translate_command_string.format(
                                        gtiff_file.name,
                                        png_file.name)
                subprocess.call(
                        translate_command,
                        stdout=fnull,
                        stderr=fnull,
                        shell=True)
                sys.stdout.write(png_file.read())
