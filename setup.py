#!/usr/bin/env python
"""
Install wagtailpolls using setuptools
"""

from wagtailpolls import __version__

with open('README.rst', 'r') as f:
    readme = f.read()

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='wagtailpolls',
    version=__version__,
    description='A polling plugin for the Wagtail CMS',
    long_description=readme,
    author='Takeflight',
    author_email='liam@takeflight.com.au',
    url='https://github.com/takeflight/wagtailpolls',

    install_requires=[
        'wagtail>=1.3',
        'django-ipware==1.1.2',
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
