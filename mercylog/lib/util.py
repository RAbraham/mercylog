from pathlib import Path


def remove_dir(a_dir: Path):
    import shutil
    shutil.rmtree(a_dir)
    pass


def tmp_folder(folder_name: str = None, prefix='delete_me') -> Path:
    import uuid
    import tempfile
    folder_name = folder_name or (prefix + '_' + str(uuid.uuid4()))

    tmp_dir = Path(tempfile.gettempdir()) / folder_name
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir
