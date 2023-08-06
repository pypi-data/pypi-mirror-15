from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.0.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name='pywinexe',
    version=__version__,
    description='A Python wrapper client for the winexe utility',
    long_description=long_description,
    url='https://github.com/tonybaloney/pywinexe',
    download_url='https://github.com/tonybaloney/pywinexe/tarball/' + __version__,
    license='APACHE2',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 2',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Anthony Shaw',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='anthony.shaw@dimensiondata.com',
    test_suite="tests",
)