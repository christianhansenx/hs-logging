from setuptools import setup, find_packages
## import codecs
## import os

VERSION = '0.0.1'
DESCRIPTION = 'A module for easily setting up standard Python logging.'

setup(
    name='hs-logging',
    version=VERSION,
    author='ChristianHansenX',
    author_email='<christian.hansen.x@gmail.com>',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyyaml'],
    keywords=['python', 'logging'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
    ]
)
