from setuptools import setup
from codecs import open
from os import path
import pyposdisplay

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyposdisplay',
    version = pyposdisplay.pyposdisplay.__version__,

    description='Python librarie for supporting Point Of Sale Display',
    long_description=long_description,

    url='https://github.com/akretion/pyposdisplay',
    author='Akretion',
    author_email='contact@akretion.com',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='bixolon lcd display pos point of sale',
    packages=['pyposdisplay'],
    install_requires=['simplejson', 'unidecode', 'pyserial'],
)
