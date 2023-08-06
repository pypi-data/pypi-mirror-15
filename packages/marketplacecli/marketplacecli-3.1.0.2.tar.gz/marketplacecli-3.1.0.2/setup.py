import os
import sys

from setuptools import setup, find_packages

from marketplacecli.utils.constants import *

# Declare your packages' dependencies here, for eg:
requires = ['uforge-marketplace_python_sdk>=3.1',
            'httplib2==0.9',
            'cmd2==0.6.7',
            'texttable>=0.8.1',
            'progressbar==2.3',
            'argparse',
            'pyparsing==2.0.2',
            'hurry.filesize==0.9',
            'termcolor==1.1.0',
            'xmlrunner==1.7.7',
            'ussclicore==1.0.1',
	    'pyxb']

if os.name != "nt":
    if "linux" not in sys.platform:
        # mac os
        requires.append('readline')
else:  # On Windows
    requires.append('pyreadline==2.0')

setup(

    install_requires=requires,

    # Fill in these to make your Egg ready for upload to
    # PyPI
    name='marketplacecli',
    version=VERSION,
    description='',
    long_description='',
    packages=find_packages(),
    author='UShareSoft',
    author_email='contac@usharesoft.com',
    license="Apache License 2.0",
    url='',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),

    # long_description= 'Long description of the package',
    scripts=['bin/marketplacecli', 'bin/marketplacecli.bat'],

)
