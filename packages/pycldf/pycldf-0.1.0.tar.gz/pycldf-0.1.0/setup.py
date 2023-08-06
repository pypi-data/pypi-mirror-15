# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requires = [
    'six',
    'pybtex',
    'clldutils',
]


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='pycldf',
    version="0.1.0",
    description='A python library to read and write CLDF datasets',
    long_description=read("README.md"),
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    url='https://github.com/glottobank/pycldf',
    install_requires=requires,
    license="Apache 2",
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages(),
    tests_require=['nose', 'coverage'],
)
