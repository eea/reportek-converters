from setuptools import find_packages, setup

setup(name='reportek.converters',
      version='1.1.3',
      author='Eau de Web',
      author_email='office@eaudeweb.ro',
      url='http://cdr.eionet.europa.eu/',

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
          'lxml==4.1.1',
          'xmltodict==0.11.0'
      ],
      #scripts=[ 'web.py', 'convert.py', 'settings.py', 'utils.py'],
      scripts=[ 'scripts/createReportekConvertersLink4Zope'],
      package_data={
          '': ['*.txt', '*.rst'],
          'reportek.converters': ['lib/*'],
      },
)
