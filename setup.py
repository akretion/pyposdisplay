from setuptools import setup, find_packages
version = open('VERSION').read().strip()

setup(
    name='pyposdisplay',
    version='0.0.4',
    author='Akretion',
    author_email='contact@akretion.com',
    url='https://github.com/akretion/pyposdisplay',
    description='Python library to support Point Of Sale displays',
    long_description=open('README.rst').read(),
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='bixolon epson lcd display pos point of sale',
    packages=find_packages(),
    install_requires=[r.strip() for r in
                      open('requirement.txt').read().splitlines()],
    include_package_data=True,
    zip_safe=False,
)
