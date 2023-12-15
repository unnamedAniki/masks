import click
from apps.main.server.commands import server_group


@click.group()
def run_group():
    pass


if __name__ == "__main__":
    run_group.add_command(server_group)
    run_group()