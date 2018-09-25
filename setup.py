#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    'pandas>=0.23.4',
]

setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]

setup(
    author="Zhuyi Xue",
    author_email='zxue@bcgsc.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="convert anntation file in GTF format to CSV format",
    entry_points={
        'console_scripts': [
            'gtf2csv=gtf2csv.gtf2csv:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='genome annotation gtf csv',
    name='gtf2csv',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/zyxue/gtf2csv',
    version='0.2',
)
