import os
import sys
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy

__version__ = '0.0.1'

COMPILE_ARGS = ["-O3", '-std=c++17', '-g',  
                '-fno-omit-frame-pointer', '-fPIC', '-g3', ]

LD_FLAGS = []

fastutil_sourcefiles = ["tinygraph/fastutils.pyx"]
extensions += [Extension("tinygraph.fastutils", fastutil_sourcefiles,
                         include_dirs=[numpy.get_include()],
                         language="c++",
                         extra_compile_args=COMPILE_ARGS, 
                         extra_link_args = LD_FLAGS, )]
setup(
    name='tinygraph',
    version=__version__,
    description='Lightweight Python library for graphs'
    url='https://github.com/thejonaslab/tinygraph',
    license='MIT',
    packages=['tinygraph'], 
    # install_requires=[
    #     'Cython>=0.29.21',
    #     'numpy>=1.19.2',
    # ],
    ext_modules = cythonize(extensions),
    include_package_data=True,
)
