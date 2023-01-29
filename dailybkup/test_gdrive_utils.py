from unittest import mock
import dailybkup.gdrive_utils as sut


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
