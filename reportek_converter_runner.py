"""Console entry point wrappers for legacy converter modules.

The historical project layout stores converter modules under
``Products/reportek.converters`` and several modules use package-relative
imports. These wrappers let installed console scripts execute those modules
without relying on Docker WORKDIR/PYTHONPATH or direct ``python path/to.py``
execution.
"""

import os
import runpy
import sys
from importlib.metadata import distribution


APP_DIR = distribution("reportek.converters").locate_file(
    "Products/reportek.converters"
)


def _prepare_path():
    app_dir = str(APP_DIR)
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)


def _run_module(module_name):
    _prepare_path()
    runpy.run_module(module_name, run_name="__main__")


def _run_script(relative_path):
    _prepare_path()
    script_path = os.path.join(str(APP_DIR), relative_path)
    sys.argv[0] = script_path
    runpy.run_path(script_path, run_name="__main__")


def gdal_export_png():
    _run_module("bin.gdal_export_png")


def gml_to_kml():
    _run_module("bin.gml_to_kml")


def gml_to_png_bg():
    _run_module("bin.gml_to_png_bg")


def gml_to_png_thumbnail_bg():
    _run_module("bin.gml_to_png_thumbnail_bg")


def mmr_p_xls_xml():
    _run_module("bin.mmr_p_xls_xml")


def xml_to_json():
    _run_module("bin.xml_to_json")


def dbf_to_html():
    _run_script("bin/converters/dbf_to_html")


def prj_as_html():
    _run_script("bin/converters/prj_as_html")


def safe_html():
    _run_script("bin/converters/safe_html")
