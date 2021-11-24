#!/usr/bin/env python

import os
from setuptools import setup, find_packages

libpath = os.path.dirname(os.path.realpath(__file__))
requirements = f"{libpath}/requirements.txt"
install_requires = []
if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

setup(
  name="weblate_exporter",
  packages=find_packages(),
  version=os.environ.get("VERSION", "dev"),
  license="GPLv3+",
  description="Weblate metrics exporter",
  long_description=open('README.md', 'r').read(),
  author="Aleksandr Loktionov",
  author_email="loktionovam@gmail.com",
  url="https://github.com/loktionovam/weblate_exporter",
  keywords=['docker', 'prometheus', 'exporter', 'weblate'],
  classifiers=[],
  python_requires=' >= 3.10',
  install_requires=install_requires,
  entry_points={
    'console_scripts': [
      'weblate_exporter=weblate_exporter.cli:main'
    ]
  }
)
