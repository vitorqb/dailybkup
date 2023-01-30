from typing import Any, Optional
import google.auth  # type: ignore
import googleapiclient.discovery  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore


class GDriveClient:
    def __init__(self, google_drive_service: Optional[Any] = None):
        """
        A Google Drive Client wrapper.
        Ref: https://developers.google.com/drive/api/quickstart/python
        """
        self._service = google_drive_service or _get_default_drive_service()

    def upload(
        self, *, parent_id: str, local_file_path: str, remote_file_name: str
    ) -> None:
        # Ref: https://developers.google.com/drive/api/guides/manage-uploads#simple
        metadata = {"name": remote_file_name, "parents": [parent_id]}
        file_ = MediaFileUpload(local_file_path)
        self._service.files().create(body=metadata, media_body=file_).execute()


def _get_default_drive_service():
    """
    Creates a google drive service using google default credential finder.
    See https://google-auth.readthedocs.io/en/master/reference/google.auth.html.
    Easiest auth mode: point GOOGLE_APPLICATION_CREDENTIALS to json file with SA.
    """
    creds, _ = google.auth.default()
    service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
    return service
