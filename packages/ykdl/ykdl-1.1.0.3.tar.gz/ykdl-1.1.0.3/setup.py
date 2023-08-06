#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except:
    from distutils.core import setup

try:
    import wheel
except:
    pass

import os, codecs

here = os.path.abspath(os.path.dirname(__file__))
README = codecs.open(os.path.join(here, 'README'), encoding='utf8').read()
CHANGES = codecs.open(os.path.join(here, 'CHANGELOG'), encoding='utf8').read()

def find_packages(*tops):
    packages = []
    for d in tops:
        for root, dirs, files in os.walk(d, followlinks=True):
            if '__init__.py' in files:
                packages.append(root)
    return packages

from ykdl.version import __version__

setup(
    name = "ykdl",
    version = __version__,
    author = "Zhang Ning",
    author_email = "zhangn1985@gmail.com",
    url = "https://github.com/zhangn1985/ykdl",
    license = "MIT",
    description = "a video downloader written in Python",
    long_description = README + '\n\n' +  CHANGES,
    keywords = "video download youtube youku",
    packages = find_packages('ykdl'),
    requires = ['m3u8'],
    install_requires = ['m3u8'],
    platforms = 'any',
    zip_safe = True,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities"
    ],
    scripts = ['bin/ykdl']
)
