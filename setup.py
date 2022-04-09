from setuptools import setup

setup(
    name='korean-geocoding',
    version='0.1.0',
    author='RE-A',
    author_email='skynine73@gmail.com',
    python_requires='>=3.6',
    install_requires=['requests'],
    description='Korean district name geocoding library',
    url="https://github.com/RE-A/korean-geocoding",
    packages=['korean_geocoding'],
    include_package_data=True
)