import os

from setuptools import setup
from setuptools.extension import Extension

try:
    import numpy as np
except ImportError:
    print("Please install numpy.")

# Dealing with Cython
USE_CYTHON = os.environ.get('USE_CYTHON', False)
ext = '.pyx' if USE_CYTHON else '.cpp'

extensions = [
    Extension('pypolyagamma.pypolyagamma',
              ['pypolyagamma/pypolyagamma' + ext],)
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    name='pypolyagamma-3',
    version='0.1.2',
    description='''Cython wrappers for Polya gamma random number generation based on Jesse
                   Windle\'s BayesLogit package: https://github.com/jwindle/BayesLogit. Forked
                   from original pypolyagamma which is authored by Scott Linderman:
                   https://github.com/slinderman/pypolyagamma.''',
    author='Matt Burbidge',
    author_email='mburbidge@savvysherpa.com',
    url='http://www.github.com/Savvysherpa/pypolyagamma',
    license="MIT",
    packages=['pypolyagamma'],
    ext_modules=extensions,
    include_dirs=[np.get_include(),],
    install_requires=[
        'numpy',
        'scipy',
        ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: C++',
        ],
    keywords=['monte-carlo', 'polya', 'gamma'],
    platforms='ALL',
)
