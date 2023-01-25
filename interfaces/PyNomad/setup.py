#!/usr/bin/env python3
# 
# 2022 - 2023 Jan Provaznik (jan@provaznik.pro)
#
# Support for statically linked PyNomad interface.

# Environment variables are used for configuration.
#
# (1) NOMAD_SRC for NOMAD source directory.
# (2) NOMAD_BUILD for NOMAD build directory.
# (3) NOMAD_VIAMSVC for signalization that MSVC will be used.
#
# Export the variables. 

import setuptools 
from Cython.Build import cythonize

import sys
import os.path
import os

# Environment processing
env_nomad_src = os.environ.get('NOMAD_SRC')
env_nomad_build_dir = os.environ.get('NOMAD_BUILD_DIR')
env_nomad_viamsvc = os.environ.get('NOMAD_VIAMSVC')

if not(env_nomad_src):
    print('Missing NOMAD_SRC env.')
    sys.exit(1)
    
if not(env_nomad_build_dir):
    print('Missing NOMAD_BUILD_DIR env.')
    sys.exit(1)

if not(env_nomad_viamsvc):
    print('Missing NOMAD_VIAMSVC, assuming GCC compatible compiler.')

# Construct paths
nomad_include_path = env_nomad_src
nomad_library_path = os.path.join(env_nomad_build_dir, 'src' , 'libnomadStatic.a')
sgtelib_library_path = os.path.join(env_nomad_build_dir,'ext', 'sgtelib','libsgtelibStatic.a')

# Version
__version__ = "unknown"
for l in open(os.path.join(nomad_include_path,'nomad_version.hpp')).readlines():
    if "#define" in l.split() and "NOMAD_VERSION_NUMBER" in l.split():
        __version__ = l.split()[-1].strip('"')
        break

# Compiler and linker configuration
# Use gcc
if (str(os.environ.get("CC")) == ""):
   os.environ["CC"] = "gcc"
if (str(os.environ.get("CXX")) == ""):
   os.environ["CXX"] = "g++"

setup_compile_args = []
setup_compile_args.append('-DNOMAD_STATIC_BUILD')

if env_nomad_viamsvc:
    setup_compile_args.append('/std:c++14')
else:
    setup_compile_args.append('-w')
    setup_compile_args.append('-std=c++14')
    setup_compile_args.append('-pthread')


setup_extra_objects = []
setup_extra_objects.append(nomad_library_path)
setup_extra_objects.append(sgtelib_library_path)
 

# Off we go.
setuptools.setup(
    name = 'PyNomad',
    version = __version__,
    author = 'Christophe Tribes',
    author_email = 'christophe.tribes@polymtl.ca',
    license = 'LGPL',
    description = 'Python interface to Nomad for blackbox optimization',
    url = 'https://github.com/bbopt/nomad',
    ext_modules = cythonize(setuptools.Extension(
        'PyNomad',
        sources = [ 'PyNomad.pyx' ],
        include_dirs = [ nomad_include_path ],
        extra_compile_args = setup_compile_args,
        extra_objects = setup_extra_objects,
        language  =  'c++'
    )),
)

