#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 14:42:06 CEST 

"""Installation instructions for shout
"""

from setuptools import setup, find_packages

setup(

    name = "shout",
    version = "0.1", 
    packages = find_packages(),

    # we also need all translation files and templates
    package_data = {
      'shout': [
        'templates/shout/*.html',
        'templates/shout/*.txt',
        'media/css/*.css',
        'media/img/*.png',
        'locale/*/LC_MESSAGES/django.po',
        'locale/*/LC_MESSAGES/django.mo',
        ],
      },

    zip_safe=False,

    install_requires = [
      'Django>=1.1',
      'docutils',
      'setuptools',
      ],

    dependency_links = [
      'http://docutils.sourceforge.net/docutils-snapshot.tgz',
      ],

    # metadata for upload to PyPI
    author = "Andre Anjos",
    author_email = "andre.dos.anjos@gmail.com",
    description = "Provides a django application that implements a simple announcement list",
    license = "PSF",
    keywords = "django announcement lists email",
    url = "",   # project home page, if any
    
)

