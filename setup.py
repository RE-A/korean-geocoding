from setuptools import find_packages, setup

setup(
    name='korean-geocoding',
    version='0.1.0',
    author='RE-A',
    author_email='skynine73@gmail.com',
    python_requires='>=3.6',
    install_requires=['requests'],
    description='Korean district name geocoding library',
    url="https://github.com/RE-A/korean-geocoding",
    package_dir={"": "korean_geocoding",
                 "data": "data"},
    packages=find_packages(where='korean_geocoding'),
)