from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

setup(
    name="indexer_python",
    version="0.2",
    author="Ganesh Katrapati",
    author_email="ganesh.katrapati@research.iiit.ac.in",
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("indexer", ["indexer.pyx", "indexer.pxd", "indexer/"])]
)
