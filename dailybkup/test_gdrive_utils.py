import pytest
from unittest import mock

# This try-catch allows us to have tests both w/ and w/out optional
# gdrive dependencies
try:
    import dailybkup.gdrive_utils as sut
except ModuleNotFoundError:
    pass


def google_drive_service_mock(*, files_pages=None):
    files_pages = files_pages or []
    page = 0

    def list_files_mock():
        nonlocal page
        try:
            next_page = files_pages[page]
        except IndexError:
            return {"nextPageToken": None, "files": []}
        page += 1
        return {
            "nextPageToken": page,
            "files": [{"name": x.name, "id": x.id} for x in next_page],
        }

    google_drive_service = mock.Mock()
    google_drive_service.files.return_value.list.return_value.execute.side_effect = (
        list_files_mock
    )
    return google_drive_service


@pytest.mark.gdrive
class TestGDriveClient:
    @mock.patch("dailybkup.gdrive_utils.MediaFileUpload")
    def test_upload_calls_service_api(self, media_file_upload_constructor):
        parent_id = "123"
        local_file_path = "/tmp/foo"
        remote_file_name = "bar"
        google_drive_service = mock.Mock()
        client = sut.GDriveClient(google_drive_service=google_drive_service)
        client.upload(
            parent_id=parent_id,
            local_file_path=local_file_path,
            remote_file_name=remote_file_name,
        )

        media_file_upload_constructor.assert_called_once_with(local_file_path)
        file_metadata = google_drive_service.files().create.call_args[1]["body"]
        assert file_metadata == {"name": remote_file_name, "parents": [parent_id]}
        media_file_upload = google_drive_service.files().create.call_args[1][
            "media_body"
        ]
        assert media_file_upload == media_file_upload_constructor()

    def test_get_files_multiple_page(self):
        google_drive_service = google_drive_service_mock(
            files_pages=[[sut.GDriveFile("foo", "id1")], [sut.GDriveFile("bar", "id2")]]
        )
        client = sut.GDriveClient(
            google_drive_service=google_drive_service, page_size=1
        )

        files = client.get_files(parent_id="PARENTID")

        assert [x for x in files] == [
            sut.GDriveFile("foo", "id1"),
            sut.GDriveFile("bar", "id2"),
        ]
        list_call_args = google_drive_service.files().list.call_args_list
        assert list_call_args[0] == mock.call(
            pageSize=1,
            fields="nextPageToken, files(id, name)",
            pageToken=None,
            q="'PARENTID' in parents",
        )
        assert list_call_args[1] == mock.call(
            pageSize=1,
            fields="nextPageToken, files(id, name)",
            pageToken=1,
            q="'PARENTID' in parents",
        )
