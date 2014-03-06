#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import shutil
from subprocess import call 
from collections import OrderedDict

# Compiler paths
FC_DEFAULT='gfortran'
MPI_DIR='/opt/mpich/3.0.4-gnu'
HDF5_DIR='/opt/hdf5/1.8.12-gnu'
PHDF5_DIR='/opt/phdf5/1.8.12-gnu'
PETSC_DIR='/opt/petsc/3.4.3-gnu'

# CTest script template
ctest_str = """set (CTEST_SOURCE_DIRECTORY "{source_dir}")
set (CTEST_BINARY_DIRECTORY "{build_dir}")

set(CTEST_SITE "{host_name}")
set (CTEST_BUILD_NAME "{build_name}")
set (CTEST_CMAKE_GENERATOR "Unix Makefiles")
set (CTEST_BUILD_OPTIONS "{build_opts}")

set(CTEST_CONFIGURE_COMMAND "${{CMAKE_COMMAND}} -H${{CTEST_SOURCE_DIRECTORY}} -B${{CTEST_BINARY_DIRECTORY}} ${{CTEST_BUILD_OPTIONS}}")
set(CTEST_MEMORYCHECK_COMMAND "/usr/bin/valgrind")
set(CTEST_MEMORYCHECK_COMMAND_OPTIONS "--tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes --track-origins=yes")

ctest_start("Nightly")
ctest_configure()
ctest_build()
ctest_test()
ctest_submit()"""

# Define test data structure
tests = OrderedDict()

class Test(object):
    def __init__(self, name, debug=False, optimize=False, mpi=False, openmp=False,
                 hdf5=False, petsc=False, valgrind=False):
        self.name = name
        self.debug = debug
        self.optimize = optimize
        self.mpi = mpi
        self.openmp = openmp
        self.hdf5 = hdf5
        self.petsc = petsc
        self.valgrind = valgrind

    def get_build_name(self):
        self.build_name = self.name
        return self.build_name

    def get_build_opts(self):
        build_str = ""
        if self.debug:
            build_str += "-Ddebug=ON "
        if self.optimize:
            build_str += "-Doptimize=ON "
        if self.openmp:
            build_str += "-Dopenmp=ON "
        if self.petsc:
            build_str += "-Dpetsc=ON "
        self.build_opts = build_str
        return self.build_opts

    def run_ctest(self, ctest_vars):
        with open('ctestscript.run', 'w') as fh:
            fh.write(ctest_str.format(**ctest_vars))

def add_test(name, debug=False, optimize=False, mpi=False, openmp=False,\
             hdf5=False, petsc=False, valgrind=False):
    tests.update({name:Test(name, debug, optimize, mpi, openmp, hdf5, petsc, valgrind)})

# List of tests
#add_test('basic-normal')
add_test('basic-debug', debug=True)
#add_test('basic-optimize', optimize=True)
#add_test('omp-normal', openmp=True)
#add_test('omp-debug', openmp=True, debug=True)
#add_test('omp-optimize', openmp=True, optimize=True)
#add_test('hdf5-normal', hdf5=True)
#add_test('hdf5-debug', hdf5=True, debug=True)
#add_test('hdf5-optimize', hdf5=True, optimize=True)
#add_test('omp-hdf5-normal', openmp=True, hdf5=True)
#add_test('omp-hdf5-debug', openmp=True, hdf5=True, debug=True)
#add_test('omp-hdf5-optimize', openmp=True, hdf5=True, optimize=True)
#add_test('mpi-normal', mpi=True)
#add_test('mpi-debug', mpi=True, debug=True)
#add_test('mpi-optimize', mpi=True, optimize=True)
#add_test('mpi-omp-normal', mpi=True, openmp=True)
#add_test('mpi-omp-debug', mpi=True, openmp=True, debug=True)
#add_test('mpi-omp-optimize', mpi=True, openmp=True, optimize=True)
#add_test('phdf5-normal', mpi=True, hdf5=True)
#add_test('phdf5-debug', mpi=True, hdf5=True, debug=True)
#add_test('phdf5-optimize', mpi=True, hdf5=True, optimize=True)
#add_test('phdf5-omp-normal', mpi=True, hdf5=True, openmp=True)
#add_test('phdf5-omp-debug', mpi=True, hdf5=True, openmp=True, debug=True)
#add_test('phdf5-omp-optimize', mpi=True, hdf5=True, openmp=True, optimize=True)
#add_test('petsc-normal', petsc=True, mpi=True)
#add_test('petsc-debug', petsc=True, mpi=True, debug=True)
#add_test('petsc-optimize', petsc=True, mpi=True, optimize=True)
#add_test('phdf5-petsc-normal', mpi=True, hdf5=True, petsc=True)
#add_test('phdf5-petsc-debug', mpi=True, hdf5=True, petsc=True, debug=True)
#add_test('phdf5-petsc-optimize', mpi=True, hdf5=True, petsc=True, optimize=True)
#add_test('omp-phdf5-petsc-normal', openmp=True, mpi=True, hdf5=True, petsc=True)
#add_test('omp-phdf5-petsc-debug', openmp=True, mpi=True, hdf5=True, petsc=True, debug=True)
#add_test('omp-phdf5-petsc-optimize', openmp=True, mpi=True, hdf5=True, petsc=True, optimize=True)

# Setup CTest vars
pwd = os.environ['PWD']
ctest_vars = {
'source_dir' : pwd + '/../src',
'build_dir' :  pwd + '/build',
'host_name' : 'bryan laptop'
}

# Begin testing
call(['rm', '-rf', 'build'])
for key in iter(tests):
    test = tests[key]

    # Set test specific CTest vars
    ctest_vars.update({'build_name' : test.get_build_name()})
    ctest_vars.update({'build_opts' : test.get_build_opts()})

    # Run test
    test.run_ctest(ctest_vars)

    # Clear build directory
    call(['rm', '-rf', 'build'])