"""uncompyle6 packaging information"""

# To the extent possible we make this file look more like a
# configuration file rather than code like setup.py. I find putting
# configuration stuff in the middle of a function call in setup.py,
# which for example requires commas in between parameters, is a little
# less elegant than having it here with reduced code, albeit there
# still is some room for improvement.

# Things that change more often go here.
copyright   = """
Copyright (C) 2015 Rocky Bernstein <rb@dustyfeet.com>.
"""

classifiers =  ['Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.6',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
                'Topic :: Software Development :: Debuggers',
                'Topic :: Software Development :: Libraries :: Python Modules',
                ]

# The rest in alphabetic order
author             = "Rocky Bernstein, Hartmut Goebel, John Aycock, and others"
author_email       = "rb@dustyfeet.com"
ftp_url            = None
# license            = 'BSDish'
mailing_list       = 'python-debugger@googlegroups.com'
modname            = 'uncompyle6'
packages           = ['uncompyle6', 'uncompyle6.opcodes', 'uncompyle6.semantics', 'uncompyle6.scanners', 'uncompyle6.parsers']
py_modules         = None
short_desc         = 'Python byte-code disassembler and source-code converter'
scripts            = ['bin/uncompyle6', 'bin/pydisassemble']

import os.path


def get_srcdir():
    filename = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))
    return os.path.realpath(filename)

ns = {}
version            = '2.3.0'
web                = 'https://github.com/rocky/python-uncompyle6/'

# tracebacks in zip files are funky and not debuggable
zip_safe = True


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description   = ( read("README.rst") + '\n' )
