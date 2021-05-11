from setuptools import setup, find_packages
version = open('VERSION', "r", encoding="utf8").read().strip()

setup(
    name='pyposdisplay',
    version=version,
    author='Akretion',
    author_email='contact@akretion.com',
    url='https://github.com/akretion/pyposdisplay',
    description='Python library to support Point Of Sale displays',
    long_description=open('README.rst', "r", encoding="utf8").read(),
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='bixolon epson lcd display pos point of sale',
    packages=find_packages(),
    install_requires=[r.strip() for r in
                      open('requirement.txt', "r", encoding="utf8").read().splitlines()],
    include_package_data=True,
    zip_safe=False,
)
