#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import autoadmin

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    author='Roberto Rosario',
    author_email='roberto.rosario.gonzalez@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    description='Automatic admin users for Django projects.',
    include_package_data=True,
    install_requires=['django-solo>=1.1.0'],
    license=license,
    long_description=readme + '\n\n' + history,
    name='django-autoadmin',
    package_data={'': ['LICENSE']},
    package_dir={'autoadmin': 'autoadmin'},
    packages=['autoadmin', 'autoadmin.migrations', 'autoadmin.templatetags', 'autoadmin.management', 'autoadmin.management.commands'],
    platforms=['any'],
    url='https://github.com/rosarior/django-autoadmin',
    version=autoadmin.__version__,
    zip_safe=False,
)
