import asyncio.events

import click
import uvicorn as uvicorn

from apps.model.settings import model_settings


@click.group('model')
def model_group():
    pass


@model_group.command(name="run")
@click.option('-m', '--model', 'AI_model',
    default=f'{model_settings.PATH}',
    help=(
        "Data path "
        "to run model"
    )
)
def run_model(model_path: str = None):
    pass

