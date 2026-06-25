1.2.12 (2026-06-25)
-------------------
* fix: fixed regression in xml_to_json for ods

1.2.11 (2026-06-25)
-------------------
* remove: obsolete GML background PNG converters that depended on unavailable ARC IMS service
* remove: unused IMS/background-map scripts and constants after dropping GML background converters

1.2.10 (2026-06-24)
-------------------
* remove: obsolete Flash converters and entry points
* remove: obsolete legacy MS Office converters based on wv/old xls/ppt tooling
* remove: obsolete GML-to-SHP/shapelib converter and inactive legacy GML scripts
* remove: unused legacy converter helper scripts, vendored GDAL wrappers, MapServer assets, and duplicate txt_to_wkt script

1.2.9 (2026-06-23)
------------------
* fix: clean metadata from xml in xml_to_json

1.2.8 (2026-06-23)
------------------
* fix: fixed xml_to_json regression
* fix: fixed tests

1.2.7 (2026-06-23)
------------------
* feat: fixed conversion scripts issues
* feat: dumped scrubber for bleach
* feat: added console_scripts entrypoints
* fix: fixed namespace

1.2.6 (2026-06-22)
------------------
* fix: fixed egg packaging

1.2.5 (2026-06-22)
------------------
* fix: added setuptools_git in requires

1.2.4 (2026-06-22)
------------------
* dependency updates, security fixes
* Fixed prj_as_html
* Fixed dbf_as_html

1.2.3 (2021-03-24)
------------------
* Updated README

1.2.2 (2021-03-24)
------------------
* Fixed README

1.2.1 (2021-03-23)
------------------
* Added MANIFEST file
* Updated setup.py

1.2.0 (2021-03-23)
------------------
* Bumped lxml
* Prep egg release

1.1.3 (2018-09-28)
------------------
* Added mmr_p_xls_xml.py script

1.1.2 (2018-05-02)
------------------
* Pinned Flask to 0.9

1.1.1 (2014-12-12)
----------------
* Preserve virtual environment across python subprocesses [baragdan]

1.1 (2014-03-07)
----------------
* Prevent safe_html from stripping i18n tags

1.0 (2014-02-07)
----------------
* Transform this product into an egg
* The start of this changelog; the rest of the changes are undocumented
