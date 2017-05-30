import setuptools
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
import pysim.info
import os.path
import sys

config = Configuration()
config.add_include_dirs([pysim.info.get_include(), numpy.get_include()])

extracompileargs = []
if sys.platform == "win32":
    config.add_include_dirs([os.environ.get('BOOST_ROOT'),
                             os.environ['EIGEN_ROOT']
                            ])
elif sys.platform == "linux":
    extracompileargs.append("-std=c++11")


cpp_ex_dir = "{{cookiecutter.project_slug}}/systems/{{cookiecutter.system_collection_slug}}"
cpp_ex_files = os.listdir(cpp_ex_dir)
cpp_ex_files = filter(lambda x: x.endswith("cpp"),cpp_ex_files)
cpp_ex_files = [os.path.join(cpp_ex_dir,x) for x in cpp_ex_files]
cpp_ex_files.append("{{cookiecutter.project_slug}}/systems/{{cookiecutter.system_collection_slug}}/{{cookiecutter.system_collection_slug}}.pyx")

extensions = [Extension("{{cookiecutter.project_slug}}.systems.{{cookiecutter.system_collection_slug}}",
                          cpp_ex_files,
                          language="c++",
                          extra_compile_args=extracompileargs,
                          include_dirs=[pysim.info.get_include(),
                                        cpp_ex_dir],
                          library_dirs=pysim.info.get_library_dir(),
                          libraries= pysim.info.get_libraries(),
                          ),
             ]

setup(
    name="{{cookiecutter.project_slug}}",
    version="0.0.1dev1",
    ext_modules=cythonize(extensions),
    packages=['{{cookiecutter.project_slug}}.systems',
              '{{cookiecutter.project_slug}}.tests',
             ],
    install_requires = ['pysim>=2.0'
                       ],
    **config.todict()
)
