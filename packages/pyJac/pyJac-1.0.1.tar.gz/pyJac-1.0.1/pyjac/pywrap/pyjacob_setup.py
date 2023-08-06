#! /usr/bin/env python2.7
from distutils.core import setup, Extension
import distutils.ccompiler

from Cython.Distutils import build_ext
import parallel_compiler as pcc
import numpy
import os

sources = ['/Users/kyle/Dropbox/Research/Code/pyJac/pyjac/pywrap/pyjacob_wrapper.pyx']
includes = ['/Users/kyle/Dropbox/Research/Code/pyJac/out/']

distutils.ccompiler.CCompiler.compile = pcc.parallel_compile

ext_modules=[Extension("pyjacob",
     sources=sources,
     include_dirs=includes + [numpy.get_include()],
     extra_compile_args=['-frounding-math', '-fsignaling-nans'],
     language='c',
     extra_objects=[os.path.join('build/temp.macosx-10.11-x86_64-2.7', '/Users/kyle/Dropbox/Research/Code/pyJac/build/temp.macosx-10.11-x86_64-2.7/libc_pyjac.a')]
     )]

setup(
    name='pyjacob',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext}
)
