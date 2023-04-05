#!/usr/bin/env python

from setuptools import find_packages, setup

requires = [
    'Flask>=2.0.1',
    'fastapi>=0.73.0',
    'contextvars>=2.3'
]

setup(
    include_package_data=True,
    name="motifer",
    version='1.1.0',
    description='Generic logs pattern builder for Python and Flask, built on top of logging module.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='Ankur Mahajan',
    author_email='mahajanankur.nith@gmail.com',
    url='https://www.searchunify.com/',
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    license="Apache License",
    python_requires=">= 3",
    project_urls={
        'Documentation': 'https://github.com/mahajanankur/motifer-py/blob/main/README.md',
        'Source': 'https://github.com/mahajanankur/motifer-py',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)