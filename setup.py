from pathlib import Path
from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A module for easily setting up standard Python logging.'

this_directory = Path(__file__).parent
long_description = (this_directory / 'README_USER.md').read_text()

setup(
    name='hs-logging',
    version=VERSION,
    author='ChristianHansenX',
    author_email='<christian.hansen.x@gmail.com>',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['testing', ]),
    install_requires=['pyyaml'],
    keywords=['python', 'logging'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
    ]
)
