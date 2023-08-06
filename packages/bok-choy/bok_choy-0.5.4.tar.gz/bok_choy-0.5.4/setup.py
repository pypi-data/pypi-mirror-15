#!/usr/bin/env python

import codecs
from setuptools import setup

VERSION = '0.5.4'
DESCRIPTION = 'UI-level acceptance test framework'
REQUIREMENTS = (
    'lazy',
    'needle',
    'selenium',
)

with codecs.open('README.rst', 'r', 'utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='bok_choy',
    version=VERSION,
    author='edX',
    author_email='oscm@edx.org',
    url='http://github.com/edx/bok-choy',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license='Apache 2.0',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Software Development :: Testing',
                 'Topic :: Software Development :: Quality Assurance'],
    packages=['bok_choy', 'bok_choy/a11y'],
    package_data={'bok_choy': ['vendor/google/*.*', 'vendor/axe-core/*.*']},
    install_requires=REQUIREMENTS,
)
