#!/usr/bin/env python3

# Start ignoring PyImportSortBear as imports below may yield syntax errors
# Stop ignoring

import locale
import sys
from subprocess import call

import setuptools.command.build_py
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

try:
    locale.getlocale()
except (ValueError, UnicodeError):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

if __name__== "__main__":
	setup(name='MockBearTest',
		  version="0.1.2",
		  description='The MockBearTest bear for coala (Code Analysis Application)',
		  author="The coala developers",
          maintainer="Lasse Schuirmann, Fabian Neuschmidt, Mischa Kruger",
          maintainer_email=('lasse.schuirmann@gmail.com, '
                            'fabian@neuschmidt.de, '
                            'makman@alice.de'),
          url='http://coala.rtfd.org/',
          platforms='any',
          packages=find_packages(exclude=("build.*", "tests", "tests.*")),
          install_requires=required,
          package_data={'bears': ["VERSION"],
                        'bears.java': ['checkstyle.jar', 'google_checks.xml'],
                        'bears.scala': ['scalastyle.jar',
                                        'scalastyle_config.xml']},
          license="AGPL-3.0",
          entry_points={"coalabears": ["coala_official_bears = bears"]},
		  classifiers=[
              'Development Status :: 4 - Beta',

              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications :: Gnome',

              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',

              'License :: OSI Approved :: GNU Affero General Public License '
              'v3 or later (AGPLv3+)',

              'Operating System :: OS Independent',

              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3 :: Only',

              'Topic :: Scientific/Engineering :: Information Analysis',
              'Topic :: Software Development :: Quality Assurance',
              'Topic :: Text Processing :: Linguistic'])