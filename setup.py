#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

package_name = 'runningbox-api-python'
package_path = os.path.abspath(os.path.dirname(__file__))
repositorty_url = 'https://gitlab.com/softbutterfly/runningbox-api---python'
long_description_file_path = os.path.join(package_path, 'README.md')
long_description = ''

try:
    with open(long_description_file_path) as f:
        long_description = f.read()
except IOError:
    pass

exec(  # pylint: disable=W0122
    open(os.path.join(package_path, 'runningbox_api', 'version.py')).read())
VERSION = locals().get('VERSION', ['0', '0', '0'])
__version__ = '.'.join(VERSION)

setup(
    name=package_name,
    packages=find_packages(
        exclude=[
            '.*',
            'docs',
            'scripts',
            'tests*',
        ]
    ),
    include_package_data=True,
    version=__version__,
    description="""Running box API Python""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SoftButterfly Development Team',
    author_email='SoftButterfly Development Team <dev@softbutterfly.io>',
    keywords=[
        'Softbutterfly',
        'Running box',
        'Running box API'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',

        'Programming Language :: Python :: 3.7',

        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url=repositorty_url,
    download_url="%(url)s/-/archive/%(version)s/%(package)s-%(version)s.tar.gz" % {
        "url": repositorty_url,
        "version": __version__,
        "package": package_name,
    },
    requires=[
        'requests',
    ],
    install_requires=[
        'requests',
    ],
)
