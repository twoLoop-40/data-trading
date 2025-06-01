import os
from pathlib import Path
from collections.abc import Callable


def get_root_dir(root_dir: str, cwd=Path.cwd()) -> str:
    # 내가 원하는 디렉토리 확인
    if os.path.basename(cwd) == root_dir:
        return cwd

    if cwd == cwd.parent:
        raise ValueError(f"Root directory '{root_dir}' not found.")

    else:
        return get_root_dir(root_dir, cwd.parent)


def make_filepath_resolver(move_to_current_root: Callable[[str], str]) -> Callable[[str, str], str]:
    def resolve_path(root_dir: str, file_path: str) -> str:
        exp_root_dir = move_to_current_root(root_dir)
        return os.path.join(exp_root_dir, file_path)

    return resolve_path
