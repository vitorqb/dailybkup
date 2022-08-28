import b2sdk.v2 as b2sdk # type: ignore
import os
import dataclasses
from typing import Optional


DELETE_ALL_FILES_WHITELIST = ["dailybkup-test"]


class B2Context:
    """
    A context class for a interacting with a B2 bucket
    """

    def __init__(
            self,
            application_key_id: str,
            application_key: str,
            bucket_name: str,
    ):
        self._bucket_name: str = bucket_name
        info = b2sdk.InMemoryAccountInfo()
        b2_api = b2sdk.B2Api(info)
        b2_api.authorize_account("production", application_key_id, application_key)
        self._b2_api = b2_api
        self._bucket = b2_api.get_bucket_by_name(bucket_name)

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    def delete_all_files(self) -> None:
        if self._bucket_name not in DELETE_ALL_FILES_WHITELIST:
            raise RuntimeError(f"Refusing to delete all files from {self._bucket_name}")
        for file_version, _ in self._bucket.ls(recursive=True):
            self._bucket.delete_file_version(file_version.id_, file_version.file_name)

    def upload(self, local_file: str, remote_file_name: str) -> None:
        self._bucket.upload_local_file(local_file, remote_file_name)

    def count_files(self) -> int:
        return sum(1 for _ in self._bucket.ls(latest_only=True, recursive=True))

    def delete(self, file_name: str) -> None:
        for file_version, _ in self._bucket.ls(recursive=True):
            if file_version.file_name == file_name:
                self._bucket.delete_file_version(file_version.id_, file_version.file_name)
