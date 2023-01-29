from typing import Any
from googleapiclient.http import MediaFileUpload  # type: ignore


class GDriveClient:
    def __init__(self, google_drive_service: Any):
        """
        A Google Drive Client wrapper.
        Ref: https://developers.google.com/drive/api/quickstart/python
        """
        self._service = google_drive_service

    def upload(
        self, *, parent_id: str, local_file_path: str, remote_file_name: str
    ) -> None:
        # Ref: https://developers.google.com/drive/api/guides/manage-uploads#simple
        metadata = {"name": remote_file_name, "parents": [parent_id]}
        file_ = MediaFileUpload(local_file_path)
        self._service.files().create(body=metadata, media_body=file_).execute()
