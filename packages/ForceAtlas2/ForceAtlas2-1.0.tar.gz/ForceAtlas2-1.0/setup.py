from distutils.core import setup

try: # If we have Cython installed
    from distutils.extension import Extension
    import Cython.Distutils
    import os
    if os.name == "nt": raise OSError
    ext_modules = [Extension('forceatlas2.fa2util', ['forceatlas2/fa2util.py', 'forceatlas2/fa2util.pxd'])]
    cmdclass = {'build_ext' : Cython.Distutils.build_ext}
    cythonopts = {"ext_modules" : ext_modules,
                  "cmdclass" : cmdclass}
except ImportError:
    print("WARNING: Cython is not installed.  If you want this to be fast, install Cython and reinstall forceatlas2.")
    cythonopts = {"py_modules" : ["forceatlas2.fa2util"]}
except OSError:
    print("WARNING: Windows and Cython don't always get along, so forceatlas2 is installing without optimizations.  Feel free to fix for your computer if you know what you're doing.")
    cythonopts = {"py_modules" : ["forceatlas2.fa2util"]}


setup(
    name = 'ForceAtlas2',
    version = '1.0',
    description = 'The ForceAtlas2 algorithm for Python (and NetworkX)',
    author = 'Max Shinn',
    author_email = 'mws41@cam.ac.uk',
    url='https://code.launchpad.net/forceatlas2-python',
    packages = ['forceatlas2'],
    requires = ['numpy'],
    **cythonopts
)
