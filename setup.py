import sys
from setuptools import setup
from setuptools import find_packages

reqs = [
  'sanic==21.9.*',
  'sh',
  'psutil==5.6.*',
  'python-consul==1.1.*',
  'redis==3.5.*',
  'aioredis==2.0.*',
  'spacy==3.4.*'
]

setup(
  name='linguist',
  version='0.1.0',
  description='Smart text processing',
  url='https://github.com/victusfate/linguist',
  author='victusfate',
  author_email='messel@gmail.com',
  license='MIT',
  packages=find_packages(),
  install_requires = reqs,
  dependency_links = [
    'git+https://github.com/victusfate/rsyslog_cee.git@main#egg=rsyslog_cee',
    'git+https://github.com/victusfate/bandolier.git@main#egg=bandolier'
  ],
  zip_safe=False
)
