
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


def convert(from_: str, to: str) -> str:
    return "sample output"


class FileConversionHandler(FileSystemEventHandler):
    """Handler for file system events that converts files when they are created or modified."""

    def __init__(self, source_pattern: str, dest: str, function: Callable):
        """
        Initialize the file conversion handler.

        Args:
            source_pattern: Glob pattern for source files (e.g., "*.md")
            dest: Destination path pattern
            function: Conversion function that takes (content, to=extension) and returns converted content
        """
        self.source_pattern = source_pattern
        self.dest_path = Path(dest)
        self.dest_dir = self.dest_path.parent
        self.function = function

        # Create destination directory if it doesn't exist
        if not self.dest_dir.exists():
            self.dest_dir.mkdir(parents=True)

    def get_dest_file(self, src_file: Path) -> Path:
        """Get the destination file path for a given source file."""
        dest_ext = self.dest_path.suffix
        return self.dest_dir / f"{src_file.stem}{dest_ext}"

    def should_process(self, src_path: Path) -> bool:
        """Check if the file matches the source pattern."""
        # Extract pattern from glob (e.g., "*.md" from source_pattern)
        # This is a simple implementation - could be enhanced for complex patterns
        if self.source_pattern.startswith("**"):
            pattern = self.source_pattern.lstrip("*").lstrip("/")
        else:
            pattern = self.source_pattern

        if pattern.startswith("*."):
            # Simple extension matching
            ext = pattern[1:]  # Remove the *
            return src_path.suffix == ext
        else:
            # For more complex patterns, use glob matching
            return src_path.match(pattern)

    def process_file(self, src_file: Path):
        """Process a single file by converting it and writing to destination."""
        if not self.should_process(src_file):
            return

        try:
            content = src_file.read_text()
            result = self.function(content, to=self.dest_path.suffix.lstrip("."))
            dest_file = self.get_dest_file(src_file)
            dest_file.write_text(result)
            print(f"Converted {src_file} to {dest_file}")
        except Exception as e:
            print(f"Error converting {src_file}: {e}")

    def on_created(self, event: FileSystemEvent):
        """Called when a file is created."""
        if not event.is_directory:
            self.process_file(Path(event.src_path))

    def on_modified(self, event: FileSystemEvent):
        """Called when a file is modified."""
        if not event.is_directory:
            self.process_file(Path(event.src_path))


def watch(source: str, dest: str, function: Callable):
    """
    Watch for file changes and convert them using the provided function.

    Args:
        source: Glob pattern for source files (e.g., "*.md")
        dest: Destination path pattern
        function: Conversion function that takes (content, to=extension) and returns converted content
    """
    # Determine the directory to watch based on the source pattern
    if source.startswith("**"):
        watch_path = "."
    else:
        # For patterns like "samples/*.md", watch "samples"
        parts = source.split("/")
        if len(parts) > 1:
            watch_path = "/".join(parts[:-1])
        else:
            watch_path = "."

    # Process existing files first
    for src_file in Path(".").glob(source):
        handler = FileConversionHandler(source, dest, function)
        handler.process_file(src_file)

    # Set up the observer
    event_handler = FileConversionHandler(source, dest, function)
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive="**" in source)

    print(f"Watching {watch_path} for changes matching {source}...")
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching.")

    observer.join()
