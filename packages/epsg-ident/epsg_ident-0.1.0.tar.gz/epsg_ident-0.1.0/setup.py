#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click',
    'flake8',
    'tox',
    'twine'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='epsg_ident',
    version='0.1.0',
    description="Quickly get the EPSG code from a .prj file or WKT",
    long_description=readme,
    author="Cory Mollet",
    author_email='cory@corymollet.com',
    url='https://github.com/cmollet/epsg_ident',
    install_requires=requirements,
    license="ISCL",
    py_modules=['epsg_ident'],
    entry_points='''
        [console_scripts]
        epsg_ident=epsg_ident:cli
        ''',
    keywords='epsg, gis, shapefile',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
