from os.path import join

from setuptools import find_packages, setup

NAME = 'reportek.converters'
PATH = ['Products', NAME, 'version.txt']
VERSION = open(join(*PATH)).read().strip()
setup(name=NAME,
      version=VERSION,
      description="Reportek converters",
      long_description_content_type="text/x-rst",
      long_description=(
          open("README.rst").read() + "\n" +
          open("CHANGELOG.rst").read()
      ),
      author='European Environment Agency: DIS1 P-Team',
      author_email='eea-edw-c-team-alerts@googlegroups.com',
      url='https://github.com/eea/reportek-converters',

      license='GPL',
      packages=find_packages(),
      py_modules=['reportek_converter_runner'],
      entry_points={
          'console_scripts': [
              'reportek-dbf-to-html=reportek_converter_runner:dbf_to_html',
              'reportek-gdal-export-png=reportek_converter_runner:gdal_export_png',
              'reportek-gml-to-kml=reportek_converter_runner:gml_to_kml',
              'reportek-mmr-p-xls-xml=reportek_converter_runner:mmr_p_xls_xml',
              'reportek-prj-as-html=reportek_converter_runner:prj_as_html',
              'reportek-safe-html=reportek_converter_runner:safe_html',
              'reportek-xml-to-json=reportek_converter_runner:xml_to_json',
          ],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'beautifulsoup4>=4.12.3',
          'bleach[css]>=6.2.0',
          'cachetools>=5.3.3',
          'path>=17.1.1',
          'Pillow>=12.2.0',
          'Flask>=3.1.3',
          'dbf>=0.94.005',
          'Jinja2>=3.1.6',
          'requests>=2.34.2',
          'openpyxl>=2.5.6',
          'jdcal>=1.4',
          'et_xmlfile>=1.0.1',
          'lxml>=6.1.1',
          'xmltodict>=0.11.0'
      ],
      package_data={
          '': ['*.txt', '*.rst'],
          'reportek.converters': ['lib/*'],
      },
)
