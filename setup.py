from setuptools import setup

# read the contents of your README file
from pathlib import Path

readme = Path(__file__).parent / 'README.md'
if readme.exists():
    with readme.open('r', encoding='utf-8') as fd:
        long_description = fd.read()
else:
    long_description = ''

setup(
    name='petal',
    version='0.0.2-1',
    packages=['petal'],
    url='https://github.com/orf/petal',
    license='MIT',
    author='Tom Forbes',
    author_email='tom@tomforb.es',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'loguru',
        'requests',
        'grpcio',
        'grpcio-tools',
        'click',
        'mypy-protobuf',
    ],
    entry_points={
        'console_scripts': [
            'petal = petal.cli:main',
            'protoc-gen-extract-streaming = petal.protoc_gen_extract_streaming:main'
        ]
    },
)
