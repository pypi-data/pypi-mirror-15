#!/usr/bin/env python
"""
uModbus is a pure Python implementation of the Modbus protocol with support
for Python 2.7, 3.3, 3.4, 3.5 and Pypy. uModbus has no runtime depedencies.

"""
import os
from setuptools import setup

cwd = os.path.dirname(os.path.abspath(__name__))

long_description = open(os.path.join(cwd, 'README.rst'), 'r').read()

setup(name='uModbus',
      version='0.5.0',
      author='Auke Willem Oosterhoff',
      author_email='oosterhoff@baopt.nl',
      description='Implementation of the Modbus protocol in pure Python.',
      url='https://github.com/AdvancedClimateSystems/umodbus/',
      long_description=long_description,
      license='MPL',
      packages=[
          'umodbus',
          'umodbus.client',
          'umodbus._functions',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Embedded Systems',
      ])
