import time
from pathlib import Path
from typing import Callable


def convert(from_: str, to: str) -> str:
    return "sample output"


def watch(source: str, dest: str, function: Callable):
    dest_path = Path(dest)
    dest_dir = dest_path.parent

    if not dest_dir.exists():
        dest_dir.mkdir(parents=True)

    def get_dest_file(src_file: Path) -> Path:
        dest_ext = dest_path.suffix
        return dest_dir / f"{src_file.stem}{dest_ext}"

    # Initial file discovery
    src_files = list(Path().glob(source))
    file_mod_times = {f: f.stat().st_mtime for f in src_files}

    while True:
        for src_file in Path().glob(source):
            mod_time = src_file.stat().st_mtime

            if (
                src_file not in file_mod_times
                or mod_time != file_mod_times[src_file]
            ):
                content = src_file.read_text()
                result = function(
                    content, to=dest_path.suffix.lstrip(".")
                )
                dest_file = get_dest_file(src_file)
                dest_file.write_text(result)
                file_mod_times[src_file] = mod_time
                print(f"Converted {src_file} to {dest_file}")
        time.sleep(1)  # Polling interval

