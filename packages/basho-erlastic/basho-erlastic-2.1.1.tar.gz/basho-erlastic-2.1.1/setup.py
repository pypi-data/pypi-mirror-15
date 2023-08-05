#!/usr/bin/env python

import setuptools

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    with open('README.rst', 'w') as f:
        f.write(long_description)
except(IOError, ImportError):
    with open('README.md') as f:
        long_description = f.read()

setuptools.setup(
    name = 'basho-erlastic',
    version = '2.1.1',
    description = 'Erlastic',
    long_description=long_description,
    author = 'Samuel Stauffer, Basho Technologies',
    author_email = 'clients@basho.com',
    url = 'http://github.com/basho/python-erlastic',
    packages = ['erlastic'],
    install_requires=['six'],
    requires=['six'],
    test_suite='tests',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
