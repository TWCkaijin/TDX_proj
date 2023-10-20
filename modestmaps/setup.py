#!/usr/bin/env python
import os
from distutils.core import setup

version = open(f'{os.getcwd()}\\ModestMaps\\VERSION', 'r').read().strip()

setup(name='ModestMaps',
      version=version,
      description='Modest Maps python port',
      author='Michal Migurski',
      url='http://modestmaps.com',
      requires=['PIL'],
      packages=['ModestMaps'],
      package_data={'ModestMaps': ['VERSION']},
      license='BSD')
