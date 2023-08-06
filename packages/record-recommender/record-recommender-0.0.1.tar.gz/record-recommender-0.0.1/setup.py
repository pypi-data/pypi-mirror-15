# -*- coding: utf-8 -*-
#
# This file is part of CERN Document Server.
# Copyright (C) 2016 CERN.
#
# CERN Document Server is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Document Server is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Document Server; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Record to Record Recommendations for Invenio."""

import os

from setuptools import find_packages, setup

readme = open('README.md').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'mock>=1.3.0',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
    'pytest-runner>=2.7.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.3',
        'sphinxcontrib-httpdomain>=1.4.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

install_requires = [
    'Click',
    'elasticsearch',
    'ipython',
    'networkx',
    'numpy',
    'pandas',
    'pyyaml',
    'raven',
    'redis',
    'simplejson',
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('record_recommender', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='record-recommender',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio recommendation',
    license='GPLv2',
    author='CERN',
    author_email='cds.support@cern.ch',
    url='https://github.com/CERNDocumentServer/record-recommender',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 2 - Pre-Alpha',
    ],
    entry_points={
        'console_scripts': [
            'recommender = record_recommender:cli',
        ]
    },
)
