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

      setup_requires = [ "setuptools_git >= 1.0", ],

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'path.py>=2.3',
          'Pillow>=6.2.2',
          'Flask>=0.12.3',
          'Flask-Script>=0.4.0',
          'dbf>=0.94.005',
          'Jinja2>=2.10',
          'argparse',
          'scrubber>=1.6.1',
          'openpyxl==2.5.6',
          'jdcal==1.4',
          'et_xmlfile==1.0.1',
          'lxml>=4.6.3',
          'xmltodict==0.11.0'
      ],
      scripts=[ 'scripts/createReportekConvertersLink4Zope'],
      package_data={
          '': ['*.txt', '*.rst'],
          'reportek.converters': ['lib/*'],
      },
)
