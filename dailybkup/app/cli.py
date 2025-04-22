import typer
import dailybkup.injector as injectormod
from dailybkup.state.state import State
from dailybkup.state.phases import Phase
import dailybkup.version as versionmod
import os.path
import os
import logging


def _get_default_config_file() -> str:
    return os.environ.get(
        "DAILYBKUP_CONFIG_FILE", os.path.expanduser("~/.config/dailybkup/config.yaml")
    )


def new_app() -> typer.Typer:
    app = typer.Typer()
    app.command()(backup)
    app.command()(version)
    app.callback()(global_setup)
    return app


def backup() -> None:
    injector = injectormod.get()
    initial_state = injector.initial_state()
    pipeline_runner = injector.pipeline_runner()
    final_state = pipeline_runner.run(initial_state)
    _handle_error(final_state)


def version() -> None:
    typer.echo(versionmod.VERSION)


def global_setup(
    config_file: str = typer.Option(_get_default_config_file(), "-c", "--config-file"),
    verbose: bool = typer.Option(False, "-v", "--verbose"),
) -> None:
    """
    Global setup for the app.
    """
    _setup_logging(verbose)
    _setup_injector(config_file)


def _setup_injector(config_file: str):
    injectormod.init(config_file=config_file)


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, handlers=[TyperLoggerHandler()], force=True)


def _handle_error(state: State):
    if state.error is None:
        return
    match state.last_phase:
        # If we fal on these steps, log the error but don't raise so we don't retry
        case Phase.CLEANUP | Phase.NOTIFICATION | Phase.END:
            logging.warning(
                f"skipping error at phase {state.last_phase}: {state.error}"
            )
            return
        # If we fail on any other step raise
        case _:
            logging.error(state.error)
            raise state.error


class TyperLoggerHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        typer.echo(self.format(record))
