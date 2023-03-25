from typing import Any, Optional, Generator, Sequence
import google.auth  # type: ignore
import googleapiclient.discovery  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore
import dataclasses
import logging


@dataclasses.dataclass
class GDriveFile:
    name: str
    id: str


class GDriveClient:
    def __init__(
        self, google_drive_service: Optional[Any] = None, page_size: int = 100
    ):
        """
        A Google Drive Client wrapper.
        Ref: https://developers.google.com/drive/api/quickstart/python
        """
        self._service = google_drive_service or _get_default_drive_service()
        self._page_size = page_size
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)

    def upload(
        self, *, parent_id: str, local_file_path: str, remote_file_name: str
    ) -> None:
        # Ref: https://developers.google.com/drive/api/guides/manage-uploads#simple
        metadata = {"name": remote_file_name, "parents": [parent_id]}
        file_ = MediaFileUpload(local_file_path)
        self._service.files().create(body=metadata, media_body=file_).execute()

    def get_files(self, *, parent_id: str) -> Generator[GDriveFile, None, None]:
        page_size = self._page_size
        page_token = None
        while True:
            api_response = (
                self._service.files()
                .list(
                    pageSize=page_size,
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                    q=f"'{parent_id}' in parents",
                )
                .execute()
            )
            for file_ in api_response.get("files", []):
                yield GDriveFile(name=file_["name"], id=file_["id"])
            page_token = api_response.get("nextPageToken", None)
            if page_token is None:
                break

    def delete_batch(self, ids_to_delete: Sequence[str]) -> None:
        for id in ids_to_delete:
            self._logger.info(f"Deleting file with id {id}")
            self._service.files().delete(fileId=id).execute()


def _get_default_drive_service():
    """
    Creates a google drive service using google default credential finder.
    See https://google-auth.readthedocs.io/en/master/reference/google.auth.html.
    Easiest auth mode: point GOOGLE_APPLICATION_CREDENTIALS to json file with SA.
    """
    creds, _ = google.auth.default()
    service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
    return service
