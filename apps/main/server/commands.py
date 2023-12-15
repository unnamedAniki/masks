import click
import uvicorn as uvicorn


@click.group('server')
def server_group():
    pass


@server_group.command(name="run")
@click.option('-h', '--host', 'uv_host',
    default='127.0.0.1',
    help=(
        "IP address or local domain name "
        "to run server on"
    )
)
@click.option('-p', '--port', 'uv_port',
    default=8000,
    help="Server port"
)
@click.option('-l', '--log-level', 'uv_log_level',
    default='info',
    help="Logging level. One of: [critical|error|warning|info|debug|trace]"
)
def run_server(
        uv_host: str = None,
        uv_port: int = None,
        uv_log_level: str = None):

    uvicorn.run("apps.run_main:app",
        host=uv_host,
        port=uv_port,
        log_level=uv_log_level,
        reload=True
    )