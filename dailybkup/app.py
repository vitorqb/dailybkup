import typer


def new_app() -> typer.Typer:
    app = typer.Typer()
    app.command()(backup)
    app.command()(version)
    return app


def backup() -> None:
    raise NotImplementedError()


def version() -> None:
    # THE NEXT LINE IS WRITTEN AUTOMATICALLY BY THE RELEASE SCRIPT. DO NOT EDIT IT.
    version = "0.0.1"  # ___VERSION___
    typer.echo(version)
