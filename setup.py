#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'networkx>=2.1',
                'Jinja2>=2.10',
                'PyYAML>=3.13',
                'Whoosh>=2.7']

setup_requirements = [ ]

test_requirements = ['tox', 'pytest']

setup(
    author="Shane William Leonard",
    author_email='shane.william.leonard@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Oz turns your documentation into context-aware shortcuts for the command line.",
    entry_points={
        'console_scripts': [
            'oz=oz.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='oz_cli',
    name='oz_cli',
    packages=find_packages(include=['oz']),
    setup_requires=setup_requirements,
    test_suite='tox',
    tests_require=test_requirements,
    url='https://github.com/shaneleonard/oz',
    version='0.3.0',
    zip_safe=False,
)
