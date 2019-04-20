import click
import os
from pathlib import Path
import importlib
import sys
import subprocess

import pkg_resources

from petal import Service
from .exceptions import InitializationException


@click.group()
def cli():
    pass


@cli.command()
@click.argument('module')
def run(module):
    sys.path.append(os.getcwd())
    module_object = importlib.import_module(module)

    try:
        app: Service = module_object.service
    except AttributeError:
        raise click.UsageError(f'Could not find {module}.service')

    try:
        app.validate_service()
    except InitializationException as e:
        raise click.ClickException(str(e))



@cli.command()
@click.argument('service_directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def build(service_directory):
    service_directory = Path(service_directory)
    proto_directory = service_directory / 'protobuf'
    if not proto_directory.exists():
        raise click.UsageError(f'{proto_directory} does not exist.')

    click.echo('Clearing output directory...')
    proto_files = set(proto_directory.glob('*.proto')) | {proto_directory / '__init__.py'}
    for path in proto_directory.iterdir():
        if path.is_file() and path not in proto_files:
            path.unlink()

    includes = []
    for entry_point in pkg_resources.iter_entry_points('petal_include_protobuf'):
        entry_point = Path(entry_point.load().__file__)
        includes.append(f'-I={entry_point.parent}')

    proto_files = [str(f.relative_to(service_directory.parent)) for f in proto_directory.glob('*.proto')]

    args = [
        'python3',
        '-m',
        'grpc_tools.protoc',
        f'--proto_path={service_directory.parent}/',
        f'--grpc_python_out={service_directory.parent}/',
        f'--python_out={service_directory.parent}/',
        f'--extract-streaming_out={service_directory.parent}/',
        f'--mypy_out={service_directory.parent}/',
        *includes,
        *proto_files
    ]
    click.echo('Compiling protobufs with ', nl=False)
    click.secho(f'{" ".join(args)}', fg='green')
    subprocess.check_call(args)


def main():
    cli()
