import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Protocol
from abc import ABC, abstractmethod
import shutil


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FileOrganizerError(Exception):
    """Custom exception for file organizer operations."""

    pass


class DateExtractor(Protocol):
    """Protocol for extracting dates from files."""

    def extract_date(self, file_path: Path) -> datetime:
        """Extract date from file."""
        ...


class ModificationDateExtractor:
    """Extracts date based on file modification time."""

    def extract_date(self, file_path: Path) -> datetime:
        """Extract date from file modification time."""
        try:
            return datetime.fromtimestamp(file_path.stat().st_mtime)
        except (OSError, ValueError) as e:
            raise FileOrganizerError(f"Cannot extract date from {file_path}: {e}")


class CreationDateExtractor:
    """Extracts date based on file creation time."""

    def extract_date(self, file_path: Path) -> datetime:
        """Extract date from file creation time."""
        try:
            # On Unix systems, st_ctime is the last metadata change time
            # For actual creation time, you might need platform-specific code
            return datetime.fromtimestamp(file_path.stat().st_ctime)
        except (OSError, ValueError) as e:
            raise FileOrganizerError(f"Cannot extract date from {file_path}: {e}")


class FileFilter(ABC):
    """Abstract base class for file filters."""

    @abstractmethod
    def should_process(self, file_path: Path) -> bool:
        """Determine if file should be processed."""
        pass


class ImageFileFilter(FileFilter):
    """Filter for image files only."""

    def __init__(self, extensions: Optional[List[str]] = None):
        self.extensions = extensions or [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".raw",
        ]

    def should_process(self, file_path: Path) -> bool:
        """Check if file is an image based on extension."""
        return file_path.suffix.lower() in self.extensions


class AllFilesFilter(FileFilter):
    """Filter that accepts all files."""

    def should_process(self, file_path: Path) -> bool:
        """Accept all files."""
        return True


class DirectoryCreator:
    """Responsible for creating directories."""

    @staticmethod
    def create_directory(path: Path) -> None:
        """Create directory if it doesn't exist."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
        except OSError as e:
            raise FileOrganizerError(f"Cannot create directory {path}: {e}")


class FileMover:
    """Responsible for moving files."""

    @staticmethod
    def move_file(source: Path, destination: Path) -> None:
        """Move file from source to destination."""
        try:
            if destination.exists():
                logger.warning(f"Destination file already exists: {destination}")
                # Create a unique name by adding a suffix
                counter = 1
                while destination.exists():
                    stem = destination.stem
                    suffix = destination.suffix
                    new_name = f"{stem}_{counter}{suffix}"
                    destination = destination.parent / new_name
                    counter += 1

            shutil.move(str(source), str(destination))
            logger.info(f"Moved file: {source} -> {destination}")
        except (OSError, shutil.Error) as e:
            raise FileOrganizerError(f"Cannot move file {source} to {destination}: {e}")


class PathValidator:
    """Validates path inputs."""

    @staticmethod
    def validate_source_path(path: Optional[str]) -> Path:
        """Validate and return source path."""
        if not path:
            raise ValueError("Path is required and cannot be empty")

        path_obj = Path(path).resolve()

        if not path_obj.exists():
            raise ValueError(f"Path does not exist: {path_obj}")

        if not path_obj.is_dir():
            raise ValueError(f"Path must be a directory: {path_obj}")

        return path_obj


class PhotoOrganizer:
    """Main class responsible for organizing photos by date."""

    def __init__(
        self,
        date_extractor: DateExtractor,
        file_filter: FileFilter,
        date_format: str = "%Y-%m-%d",
    ):
        self.date_extractor = date_extractor
        self.file_filter = file_filter
        self.date_format = date_format
        self.directory_creator = DirectoryCreator()
        self.file_mover = FileMover()
        self.path_validator = PathValidator()

    def organize(self, source_path: str, dry_run: bool = False) -> None:
        """
        Organize files in the source path by date.

        Args:
            source_path: Path to the source directory
            dry_run: If True, only log what would be done without actual file operations
        """
        try:
            validated_path = self.path_validator.validate_source_path(source_path)
            logger.info(f"Starting organization of: {validated_path}")

            files_to_process = self._get_files_to_process(validated_path)

            if not files_to_process:
                logger.info("No files to process")
                return

            logger.info(f"Found {len(files_to_process)} files to process")

            for file_path in files_to_process:
                self._process_file(file_path, validated_path, dry_run)

            logger.info("Organization completed successfully")

        except (ValueError, FileOrganizerError) as e:
            logger.error(f"Organization failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during organization: {e}")
            raise FileOrganizerError(f"Unexpected error: {e}")

    def _get_files_to_process(self, source_path: Path) -> List[Path]:
        """Get list of files that should be processed."""
        try:
            return [
                file_path
                for file_path in source_path.iterdir()
                if file_path.is_file() and self.file_filter.should_process(file_path)
            ]
        except OSError as e:
            raise FileOrganizerError(f"Cannot read directory {source_path}: {e}")

    def _process_file(self, file_path: Path, base_path: Path, dry_run: bool) -> None:
        """Process a single file."""
        try:
            file_date = self.date_extractor.extract_date(file_path)
            folder_name = file_date.strftime(self.date_format)
            destination_folder = base_path / folder_name
            destination_file = destination_folder / file_path.name

            if dry_run:
                logger.info(f"[DRY RUN] Would move: {file_path} -> {destination_file}")
                return

            self.directory_creator.create_directory(destination_folder)
            self.file_mover.move_file(file_path, destination_file)

        except FileOrganizerError:
            logger.error(f"Failed to process file: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing file {file_path}: {e}")
            raise FileOrganizerError(f"Unexpected error processing {file_path}: {e}")


def create_photo_organizer() -> PhotoOrganizer:
    """Factory function to create a PhotoOrganizer with default configuration."""
    date_extractor = ModificationDateExtractor()
    file_filter = ImageFileFilter()
    return PhotoOrganizer(date_extractor, file_filter)


def main():
    """Main function to run the photo organizer."""
    try:
        organizer = create_photo_organizer()
        source_path = "/home/adrian/Pictures/camera/"

        # First run as dry run to see what would happen
        logger.info("Running dry run...")
        organizer.organize(source_path, dry_run=False)

        # Uncomment the line below to actually move files
        # organizer.organize(source_path, dry_run=False)

    except Exception as e:
        logger.error(f"Application failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
