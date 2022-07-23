import typer
import dailybkup.injector as injector
import os.path
import os


def _get_default_config_file() -> str:
    return os.environ.get(
        "DAILYBKUP_CONFIG_FILE",
        os.path.expanduser("~/.dailybkup/config.yaml")
    )


def new_app() -> typer.Typer:
    app = typer.Typer()
    app.command()(backup)
    app.command()(version)
    app.callback()(injector_cbk)
    return app


def backup() -> None:
    injector.get().runner().run()


def version() -> None:
    # THE NEXT LINE IS WRITTEN AUTOMATICALLY BY THE RELEASE SCRIPT. DO NOT EDIT IT.
    version = "0.0.1"  # ___VERSION___
    typer.echo(version)


def injector_cbk(
        config_file: str = typer.Option(_get_default_config_file, "-c", "--config-file")
) -> None:
    injector.init(config_file=config_file)
