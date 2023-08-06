#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'requests==2.10.0',
    'ujson==1.35',
    'inflect==0.2.5',
    'six==1.10.0'
]

test_requirements = [
]

setup(
    name='beckett',
    version='0.3.0',
    description="Hypermedia driven API Client Framework",
    long_description=readme + '\n\n' + history,
    author="Paul Hallett",
    author_email='paulandrewhallett@gmail.com',
    url='https://github.com/phalt/beckett',
    packages=[
        'beckett',
    ],
    package_dir={'beckett':
                 'beckett'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='beckett',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
