from distutils.core import setup

from os.path import abspath, dirname, join
execfile(join(dirname(abspath(__file__)), 'target', 'src', 'SikuliLibrary', 'version.py'))

# import os

DESCRIPTION = """
Sikuli Robot Framework Library provide keywords for Robot Framework to test UI through Sikuli.

Notes: SikuliLibrary.jar file is OS dependent. The version for Windows 64bit is included.
If target OS is not Windows, please get source code from GITHUB, and use Maven to build
SikuliLibrary.jar on target OS, and replace the jar file in 'lib' folder.
"""[1:-1]
CLASSIFIERS = """
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Java
Topic :: Software Development :: Testing
"""[1:-1]

# compile_cmd ='mvn package'
# print('*************************** '+compile_cmd+' ***************************') 
# os.system(compile_cmd)

# print("*************************** setup.py install ***************************")

setup(name         = 'RobotSikuliLibrary',
      version      = '1.0.4',
      description  = 'Sikuli library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Whitney0323',
      author_email = 'Whitney0323@163.com',
      url          = 'https://github.com/bluesummerbreeze/robotframework-SikuliLibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation sikuli UI',
      platforms    = 'any',
      classifiers  = CLASSIFIERS.splitlines(),
      package_dir  = {'' : 'target/src'},
      packages     = ['SikuliLibrary'],
      package_data = {'SikuliLibrary': ['lib/*.jar',
                                          ]},
      )