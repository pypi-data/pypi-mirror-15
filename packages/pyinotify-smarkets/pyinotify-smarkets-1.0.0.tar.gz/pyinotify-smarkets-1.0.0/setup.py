#!/usr/bin/env python

# Set True to force compile native C-coded extension providing direct access
# to inotify's syscalls. If set to False this extension will only be compiled
# if no inotify interface from ctypes is found.
compile_ext_mod = False

# import statements
import os
import sys
import distutils.extension
from distutils.util import get_platform
try:
    # First try to load most advanced setuptools setup.
    from setuptools import setup
except:
    # Fall back if setuptools is not installed.
    from distutils.core import setup

platform = get_platform()

# check Python's version
if sys.version_info < (3, 5):
    sys.stderr.write('This module requires at least Python 3.5\n')
    sys.exit(1)

classif = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Filesystems',
    'Topic :: System :: Monitoring',
    ]


def should_compile_ext_mod():
    try:
        import ctypes
        import ctypes.util
    except:
        return True

    try_libc_name = 'c'
    if platform.startswith('freebsd'):
        try_libc_name = 'inotify'

    libc_name = None
    try:
        libc_name = ctypes.util.find_library(try_libc_name)
    except:
        pass  # Will attemp to load it with None anyway.

    libc = ctypes.CDLL(libc_name)
    # Eventually check that libc has needed inotify bindings.
    if (not hasattr(libc, 'inotify_init') or
        not hasattr(libc, 'inotify_add_watch') or
        not hasattr(libc, 'inotify_rm_watch')):
        return True
    return False


ext_mod = []
if compile_ext_mod or should_compile_ext_mod():
    # add -fpic if x86_64 arch
    if platform in ["linux-x86_64"]:
        os.environ["CFLAGS"] = "-fpic"
    # sources for ext module
    ext_mod_src = ['common/inotify_syscalls.c']
    # dst for ext module
    ext_mod.append(distutils.extension.Extension('inotify_syscalls',
                                                 ext_mod_src))


setup(
    name='pyinotify-smarkets',
    version='1.0.0',
    description='Linux filesystem events monitoring',
    author='Sebastien Martini',
    author_email='seb@dbzteam.org',
    maintainer='Smarkets Limited',
    maintainer_email='support@smarkets.com',
    license='MIT License',
    platforms='Linux',
    classifiers=classif,
    url='http://github.com/smarkets/pyinotify-smarkets',
    download_url='http://pypi.python.org/pypi/pyinotify-smarkets',
    ext_modules=ext_mod,
    py_modules=['pyinotify'],
    )
