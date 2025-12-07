#!/usr/bin/env python
"""
A helper script that allows you to test whether the google drive client is working.
"""
import logging
import typer
from dailybkup import b2utils

app = typer.Typer()


@app.callback()
def setup(
    ctx: typer.Context,
    application_key_id: str = typer.Option(
        ..., envvar="DAILYBKUP_B2_APPLICATION_KEY_ID"
    ),
    application_key: str = typer.Option(..., envvar="DAILYBKUP_B2_APPLICATION_KEY"),
    bucket_name: str = typer.Option(..., envvar="DAILYBKUP_B2_BUCKET_NAME"),
    prefix: str = typer.Option("", envvar="DAILYBKUP_B2_PREFIX"),
    log_level: str = typer.Option("DEBUG", envvar="LOG_LEVEL"),
):
    logging.basicConfig(level=log_level)
    b2context = b2utils.B2Context(
        application_key_id=application_key_id,
        application_key=application_key,
        bucket_name=bucket_name,
        prefix=prefix,
    )
    ctx.obj = b2context


@app.command()
def delete_file(file_name: str, ctx: typer.Context):
    """
    Delete a file from the bucket based on it's name.
    """
    b2context = ctx.obj
    b2context.delete(file_name)


if __name__ == "__main__":
    app()
