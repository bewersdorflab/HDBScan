#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='hdbscan',
      version='0.1',
      description='Taking the hdbscan package and making a callable module in visgui',
      author='Ben Rollins',
      author_email='bennett.rollins@yale.edu',
      packages=find_packages()
      # package_data={
      #       # include all svg and html files, otherwise conda will miss them
      #       '': ['*.svg', '*.html'],
      # }
     )
