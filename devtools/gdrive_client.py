#!/usr/bin/env python
"""
A helper script that allows you to test whether the google drive client is working.
"""
import typer
import dailybkup.gdrive_utils as gdrive_utils
import google.auth  # type: ignore
import googleapiclient.discovery  # type: ignore


GOOGLE_APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"
app = typer.Typer()
client = None


@app.callback()
def setup(
    service_account_json_file: str = typer.Option(
        None, envvar=GOOGLE_APPLICATION_CREDENTIALS
    )
):
    global client
    assert service_account_json_file
    google_credentials, _ = google.auth.load_credentials_from_file(
        service_account_json_file
    )
    google_drive_service = googleapiclient.discovery.build(
        "drive", "v3", credentials=google_credentials
    )
    client = gdrive_utils.GDriveClient(
        google_drive_service=google_drive_service, page_size=2
    )


@app.command()
def list(parent_id: str = typer.Option(...)):
    assert client
    for file_ in client.get_files(parent_id=parent_id):
        print(file_)


@app.command()
def upload(
    parent_id: str = typer.Option(...),
    remote_file_name: str = typer.Option("foo"),
    local_file_path: str = typer.Argument(...),
):
    assert client
    client.upload(
        parent_id=parent_id,
        local_file_path=local_file_path,
        remote_file_name=remote_file_name,
    )


@app.command()
def delete(file_id: str = typer.Option(...)):
    assert client
    client.delete_batch([file_id])


if __name__ == "__main__":
    app()
