# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(name = 'timeago',
      version = '1.0.3',
      description = 'A python lib format datetime to *** time ago',
      long_description = '',
      author = 'hustcc',
      author_email = 'i@hust.cc',
      url = 'https://github.com/hustcc/timeago',
      license = 'MIT',
      install_requires = [],
      classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
      ],
      keywords = 'timeago, seconds ago, minutes ago, hours ago, just now',
      packages = find_packages('src'),
      package_dir = {'':'src'},
)
