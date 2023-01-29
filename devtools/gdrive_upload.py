"""
A helper script that allows you to test whether the google drive client is working.
"""
import typer
import os
import dailybkup.gdrive_utils as gdrive_utils


GOOGLE_APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"


def main(
    parent_id: str = typer.Option(...),
    remote_file_name: str = typer.Option("foo"),
    service_account_json_file: str = typer.Option(
        None, envvar="GOOGLE_APPLICATION_CREDENTIALS"
    ),
    local_file_path: str = typer.Argument(...),
):
    assert service_account_json_file
    os.environ.setdefault(GOOGLE_APPLICATION_CREDENTIALS, service_account_json_file)
    client = gdrive_utils.GDriveClient()
    client.upload(
        parent_id=parent_id,
        local_file_path=local_file_path,
        remote_file_name=remote_file_name,
    )


if __name__ == "__main__":
    typer.run(main)
