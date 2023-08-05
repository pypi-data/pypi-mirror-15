"""
PyPi Setup file.
"""
# pylint: disable=no-name-in-module, import-error
from distutils.core import setup
from django_g11n.__info__ import VERSION
BASE_URL = "https://bitbucket.org/hellwig/django-g11n"

setup(
  name = 'Django-G11N',
  packages = ['django_g11n'],
  version = VERSION,
  description = 'Django Globalisation Tools',
  author = 'Martin P. Hellwig',
  author_email = 'martin.hellwig@gmail.com',
  url = BASE_URL,
  download_url = BASE_URL + '/get/' + VERSION + '.zip',
  keywords = ['django'],
  license = 'BSD',
  classifiers = ['Programming Language :: Python :: 3',],
  install_requires = ['Django>=1.9.6',
                      'django-countries>=3.4.1',
                      'django-ipware>=1.1.5',
                      'django-integrator>=0.1.0',
                      'requests>=2.10.0'],
)