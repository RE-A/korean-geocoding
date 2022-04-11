from setuptools import setup

long_description = """
"Please view usage and document on https://github.com/RE-A/korean-geocoding.
사용법과 문서는 위 링크를 참조해 주세요."
"""

setup(
    name='korean-geocoding',
    version='0.2.0',
    author='RE-A',
    author_email='skynine73@gmail.com',
    python_requires='>=3.6',
    install_requires=['requests', 'haversine'],
    description='Korean district name geocoding library',
    long_description=long_description,
    url="https://github.com/RE-A/korean-geocoding",
    packages=['korean_geocoding'],
    include_package_data=True
)