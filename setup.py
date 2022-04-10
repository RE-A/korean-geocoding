from setuptools import setup

setup(
    name='korean-geocoding',
    version='0.1.3',
    author='RE-A',
    author_email='skynine73@gmail.com',
    python_requires='>=3.6',
    install_requires=['requests'],
    description='Korean district name geocoding library',
    long_description= "Please view usage and document on https://github.com/RE-A/korean-geocoding.",
    url="https://github.com/RE-A/korean-geocoding",
    packages=['korean_geocoding'],
    include_package_data=True
)