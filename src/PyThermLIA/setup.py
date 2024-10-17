with open('README.rst', 'r') as f:
    readme = f.read()
    
from setuptools import setup, Extension
from pyThermLIA import __version__
import numpy
if __name__ == '__main__':
    setup(name='pyThermLIA',
        version=__version__,
        author='Eduardo Vargas Bernardino',
        author_email='odinyzeus@live.com.mx',
        description='Digital Lock In Amplifier library',
        url='https://github.com/LolloCappo/pyLIA',
        py_modules=['pyThermLIA'],
        long_description=readme,
        install_requires = 'numpy , opencv'
      )