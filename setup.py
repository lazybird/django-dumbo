from setuptools import setup, find_packages

import dumbo


setup(
    name='django-dumbo',
    version=dumbo.__version__,
    description=dumbo.__doc__,
    packages=find_packages(),
    url='http://github.com/lazybird/django-dumbo/',
    author='lazybird',
    long_description=open('README.md').read(),
    include_package_data=True,
)
