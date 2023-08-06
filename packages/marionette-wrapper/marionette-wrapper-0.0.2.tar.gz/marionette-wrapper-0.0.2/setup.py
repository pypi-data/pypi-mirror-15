# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import io
import os
from setuptools import setup, find_packages

PACKAGE_VERSION = '0.0.2'

deps = [
    'marionette-client == 2.0.0',
    'marionette-driver == 1.1.1',
    'mozfile == 1.2',
    'mozinfo == 0.8',
    'mozinstall == 1.12',
    'mozlog == 3.0',
    'pytest == 2.7.3'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf8') as f:
    README = f.read()

setup(name='marionette-wrapper',
      version=PACKAGE_VERSION,
      description='A wrapper for Marionette that increases test legibility',
      long_description='See https://github.com/mozilla-services/services-test/tree/dev/services-marionette',  # noqa
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',  # noqa
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',  # noqa
                   ],
      keywords='mozilla services',
      author='Mozilla Cloud Services QA Team',
      author_email='cloud-services-qa@mozilla.com',
      url='https://github.com/mozilla-services/marionette-wrapper',  # noqa
      license='MPL 2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps)
