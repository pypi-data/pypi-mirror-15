#!/usr/bin/env python
from __future__ import unicode_literals
from csv_generator import __version__
from setuptools import setup, find_packages

setup(
      name='csv_generator',
      version=__version__,
      description='Configurable CSV Generator for Django',
      author='Dan Stringer',
      author_email='dan.stringer1983@googlemail.com',
      url='https://github.com/fatboystring/csv_generator/',
      packages=find_packages(exclude=['app']),
      license='MIT',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
      ],
      data_files=[
            ('templates', ['admin/csv_generator/csv_generator_select.html'])
      ],
      keywords='csv generator queryset django',
      install_requires=[],
)
