#!/usr/bin/env python

from __future__ import absolute_import
from distutils.core import setup
from distutils.errors import DistutilsSetupError


def _get_version():
    try:
        with open('VERSION') as f:
            return f.read().strip()
    except IOError:
        raise DistutilsSetupError('failed to read version info')


setup(
    name='spiddjango',
    version=_get_version(),
    description='SPID Service Provider Django Application',
    long_description='SPID Service Provider Django Application',
    author='Vittorio Meloni',
    author_email='vittorio.meloni@crs4.it',
    url='https://github.com/crs4/spid-django',
    download_url='https://github.com/crs4/spid-django',
    install_requires=[
        'djangosaml2',
    ],
    keywords=['SPID', 'SAML2', 'Django'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['spiddjango', 'spiddjango.migrations', 'spiddjango.templatetags'],
    package_dir={'spiddjango': 'spiddjango'},
    package_data={'spiddjango': ['saml2/attribute-maps/*.py',
                                 'spid-idp-metadata/*.xml',
                                 'static/spid/css/*.css',
                                 'static/spid/img/*',
                                 'static/spid/js/*.js',
                                 'templates/*']},
    include_package_data=True
)
