from pathlib import Path
from datetime import datetime


def order_path(path: str) -> None:

    if path is None or path == "":
        raise ValueError("Path is required")

    p = Path(path)

    if not p.exists() or not p.is_dir():
        raise ValueError("Path must exist and be a directory")

    for file in [file for file in p.iterdir() if file.is_file()]:
        creation_date = datetime.fromtimestamp(file.stat().st_mtime)
        destination_path_folder_name = creation_date.strftime("%Y-%m-%d")
        path_dir = f"{path}{destination_path_folder_name}"
        dir_path = Path(path_dir)
        if not dir_path.exists():
            dir_path.mkdir()

        print(f"Moving file {file} to {path_dir}/{file.name}")
        file.rename(f"{path_dir}/{file.name}")


if __name__ == "__main__":
    path = "/home/adrian/Pictures/camera/"
    order_path(path)