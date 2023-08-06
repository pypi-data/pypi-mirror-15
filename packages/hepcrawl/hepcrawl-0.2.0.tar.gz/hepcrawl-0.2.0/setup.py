# -*- coding: utf-8 -*-
#
# This file is part of hepcrawl.
# Copyright (C) 2015, 2016 CERN.
#
# hepcrawl is a free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Scrapy project for feeds into INSPIRE-HEP (http://inspirehep.net)."""

import os

from setuptools import setup, find_packages

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

install_requires = [
    'Scrapy>=1.1.0',
    'scrapyd>=1.1.0',
    'scrapyd-client>=1.0.1',
    'six>=1.9.0',
    'HarvestingKit>=0.6.3',
    'requests>=2.8.1',
    'celery>=3.1.23',
]

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'pytest>=2.8.0',
    'pytest-cov>=2.1.0',
    'pytest-pep8>=1.0.6',
    'pytest-runner>=2.7.0',
    'responses>=0.5.0'
]

extras_require = {
    'docs': [
        'Sphinx>=1.4',
        'Sphinx-PyPI-upload>=0.2.1',
    ],
    'tests': tests_require,
    'sentry': [
        'raven==5.1.1',
        'scrapy-sentry',
    ],
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('hepcrawl', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='hepcrawl',
    version=version,
    packages=find_packages(),
    description=__doc__,
    long_description=readme + '\n\n' + history,
    url='https://github.com/inspirehep/hepcrawl',
    author="CERN",
    author_email='admin@inspirehep.net',
    entry_points={'scrapy': ['settings = hepcrawl.settings']},
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Framework :: Scrapy',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
