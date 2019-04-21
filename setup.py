from setuptools import setup

setup(
    name='petal',
    version='0.0.2',
    packages=['petal'],
    url='',
    license='',
    author='Tom Forbes',
    author_email='',
    description='',
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
