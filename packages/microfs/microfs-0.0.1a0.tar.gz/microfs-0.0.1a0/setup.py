#!/usr/bin/env python3
from setuptools import setup
from microfs import get_version


with open('README.rst') as f:
    readme = f.read()
with open('CHANGES.rst') as f:
    changes = f.read()


description = ('A module and utility to work with the simple filesystem on '
               'the BBC micro:bit')


setup(
    name='microfs',
    version=get_version(),
    description=description,
    long_description=readme + '\n\n' + changes,
    author='Nicholas H.Tollervey',
    author_email='ntoll@ntoll.org',
    url='https://github.com/ntoll/microfs',
    py_modules=['microfs', ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Education',
        'Topic :: Software Development :: Embedded Systems',
    ],
    entry_points={
        'console_scripts': ['ufs=microfs:main'],
    }
)
