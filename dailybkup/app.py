import typer
import dailybkup.injector as injector
import os.path
import os
import logging


def _get_default_config_file() -> str:
    return os.environ.get(
        "DAILYBKUP_CONFIG_FILE",
        os.path.expanduser("~/.dailybkup/config.yaml")
    )


def new_app() -> typer.Typer:
    app = typer.Typer()
    app.command()(backup)
    app.command()(version)
    app.callback()(global_setup)
    return app


def backup() -> None:
    injector.get().runner().run()


def version() -> None:
    # THE NEXT LINE IS WRITTEN AUTOMATICALLY BY THE RELEASE SCRIPT. DO NOT EDIT IT.
    version = "0.0.1"  # ___VERSION___
    typer.echo(version)


def global_setup(
        config_file: str = typer.Option(_get_default_config_file(), "-c", "--config-file"),
        verbose: bool = typer.Option(False, "-v", "--verbose")
) -> None:
    """
    Global setup for the app.
    """
    _setup_logging(verbose)
    _setup_injector(config_file)


def _setup_injector(config_file: str):
    injector.init(config_file=config_file)


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)
