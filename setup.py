#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'pcapy',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='wifijammer',
    version='0.1.0',
    description="Continuously jam all wifi clients/routers",
    long_description=readme + '\n\n' + history,
    author="Dan McInerney",
    author_email='danhmcinerney@gmail.com',
    url='https://github.com/DanMcInerney/wifijammer',
    packages=[
        'wifijammer',
    ],
    package_dir={'wifijammer':
                 'wifijammer'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='wifijammer',
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
    ],
    scripts=[
        'wifijammer/wifijammer.py'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
