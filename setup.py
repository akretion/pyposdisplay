from setuptools import setup
version = open('VERSION').read().strip()

setup(
    name='pyposdisplay',
    version='0.0.2',
    author='Akretion',
    author_email='contact@akretion.com',
    url='https://github.com/akretion/pyposdisplay',
    description='Python librarie for supporting Point Of Sale Display',
    long_description=open('README.md').read(),
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='bixolon lcd display pos point of sale',
    packages=['pyposdisplay'],
    install_requires=[r.strip() for r in
                      open('requirement.txt').read().splitlines()],
)
