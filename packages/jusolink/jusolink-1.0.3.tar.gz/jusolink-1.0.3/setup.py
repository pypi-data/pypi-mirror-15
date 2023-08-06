from __future__ import print_function

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

version = '1.0.3'

if sys.version_info <= (2, 5):
    error = "ERROR: jusolink requires Python Version 2.6 or above...exiting."
    print(error, file=sys.stderr)
    sys.exit(1)

setup(name = "jusolink",
      version = version,
      description = "Jusolink API SDK Library",
      long_description = "Juslink API SDK. Consist of Taxinvice Service. http://www.jusolink.com",
      author = "Jeong Yohan",
      author_email = "yhjeong@linkhub.co.kr",
      url = "https://github.com/linkhub-sdk/Jusolink.py",
      download_url = "https://github.com/linkhub-sdk/Jusolink.py/archive/"+version+".tar.gz",
      packages = ["jusolink"],
      install_requires=[
          'linkhub',
      ],
      license = "MIT",
      platforms = "Posix; MacOS X; Windows",
      classifiers = ["Development Status :: 5 - Production/Stable",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Topic :: Internet",
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 2.6",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.3",
                     "Programming Language :: Python :: 3.4"]
      )
