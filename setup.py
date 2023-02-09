#!/usr/bin/env python

from setuptools import find_packages, setup

requires = [
    'requests==2.23.0', 
    'schema==0.7.4'
]

setup(
    include_package_data=True,
    name="motifer",
    version='1.0.0',
    description='The SearchUnify SDK enables developers to easily work with the SearchUnify platform and build scalable solutions with search, analytics, crawlers and more.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='SearchUnify',
    author_email='ankur.mahajan@grazitti.com',
    url='https://www.searchunify.com/',
    packages=find_packages(exclude=['tests*']),
    install_requires=requires,
    license="MIT",
    python_requires=">= 3",
    project_urls={
        'Documentation': 'https://docs.searchunify.com/Content/Developer-Guides/SDKs-Python.htm',
        'Source': 'https://github.com/searchunify/su-sdk-python',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)