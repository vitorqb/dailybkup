from typing import List
import subprocess


def list_files(tar_file: str) -> List[str]:
    output = subprocess.check_output(["tar", "-tf", tar_file])
    return output.decode().splitlines()
