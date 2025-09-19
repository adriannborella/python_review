# Photo Organizer

A Python script to organize photos by date into separate folders.

## Features

- Organizes photos by modification or creation date
- Supports multiple image formats
- Configurable date formats
- Dry run mode for safe testing
- Comprehensive error handling and logging
- Handles duplicate file names
- Extensible architecture with SOLID principles

## Architecture Improvements

The improved version follows Object-Oriented Programming (OOP) and SOLID principles:

### SOLID Principles Applied:

1. **Single Responsibility Principle (SRP)**:
   - `DirectoryCreator`: Only creates directories
   - `FileMover`: Only moves files
   - `PathValidator`: Only validates paths
   - `DateExtractor`: Only extracts dates from files

2. **Open/Closed Principle (OCP)**:
   - `FileFilter` abstract base class allows extending with new filter types
   - `DateExtractor` protocol allows different date extraction strategies

3. **Liskov Substitution Principle (LSP)**:
   - Any `FileFilter` implementation can be substituted
   - Any `DateExtractor` implementation can be substituted

4. **Interface Segregation Principle (ISP)**:
   - Small, focused interfaces like `DateExtractor` protocol
   - Clients only depend on methods they use

5. **Dependency Inversion Principle (DIP)**:
   - `PhotoOrganizer` depends on abstractions (`DateExtractor`, `FileFilter`)
   - High-level modules don't depend on low-level modules

### Defensive Programming Features:

- **Input Validation**: All inputs are validated before processing
- **Error Handling**: Comprehensive exception handling with custom exceptions
- **Logging**: Detailed logging for debugging and monitoring
- **Dry Run Mode**: Test operations without actual file modifications
- **Duplicate Handling**: Automatic renaming when destination files exist
- **Resource Safety**: Using `shutil.move()` instead of `Path.rename()` for safer operations

## Usage

```python
from main_improved import create_photo_organizer

# Create organizer with default settings
organizer = create_photo_organizer()

# Test with dry run first
organizer.organize("/path/to/photos", dry_run=True)

# Actually organize files
organizer.organize("/path/to/photos", dry_run=False)
```

## Customization

```python
from main_improved import (
    PhotoOrganizer, ModificationDateExtractor, 
    ImageFileFilter, AllFilesFilter
)

# Custom configuration
date_extractor = ModificationDateExtractor()
file_filter = AllFilesFilter()  # Process all files, not just images
custom_organizer = PhotoOrganizer(
    date_extractor, 
    file_filter, 
    date_format="%Y/%m"  # Year/Month folders
)
```

## Testing

Run the test suite:

```bash
python test_photo_organizer.py
```

## Configuration

Edit `config.py` to customize default settings:
- Date format for folder names
- Supported image extensions
- Default source path
- Logging configuration
