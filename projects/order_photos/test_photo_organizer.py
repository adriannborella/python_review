import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime

# Import the classes from the main module
import sys
sys.path.append('/home/adrian/projects/ab_order_photos')
from main_improved import (
    PhotoOrganizer, ModificationDateExtractor, ImageFileFilter,
    PathValidator, DirectoryCreator, FileMover, FileOrganizerError
)


class TestModificationDateExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = ModificationDateExtractor()
    
    def test_extract_date_success(self):
        # Mock file path and stat
        mock_path = Mock(spec=Path)
        mock_stat = Mock()
        mock_stat.st_mtime = 1609459200  # 2021-01-01 00:00:00 UTC
        mock_path.stat.return_value = mock_stat
        
        result = self.extractor.extract_date(mock_path)
        
        self.assertIsInstance(result, datetime)
    
    def test_extract_date_file_not_found(self):
        mock_path = Mock(spec=Path)
        mock_path.stat.side_effect = OSError("File not found")
        
        with self.assertRaises(FileOrganizerError):
            self.extractor.extract_date(mock_path)


class TestImageFileFilter(unittest.TestCase):
    
    def setUp(self):
        self.filter = ImageFileFilter()
    
    def test_should_process_image_file(self):
        mock_path = Mock(spec=Path)
        mock_path.suffix = '.jpg'
        
        result = self.filter.should_process(mock_path)
        
        self.assertTrue(result)
    
    def test_should_not_process_non_image_file(self):
        mock_path = Mock(spec=Path)
        mock_path.suffix = '.txt'
        
        result = self.filter.should_process(mock_path)
        
        self.assertFalse(result)
    
    def test_case_insensitive_extension(self):
        mock_path = Mock(spec=Path)
        mock_path.suffix = '.JPG'
        
        result = self.filter.should_process(mock_path)
        
        self.assertTrue(result)


class TestPathValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = PathValidator()
    
    def test_validate_empty_path(self):
        with self.assertRaises(ValueError):
            self.validator.validate_source_path("")
    
    def test_validate_none_path(self):
        with self.assertRaises(ValueError):
            self.validator.validate_source_path(None)
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    def test_validate_valid_path(self, mock_is_dir, mock_exists):
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        
        result = self.validator.validate_source_path("/valid/path")
        
        self.assertIsInstance(result, Path)


class TestPhotoOrganizer(unittest.TestCase):
    
    def setUp(self):
        self.mock_date_extractor = Mock()
        self.mock_file_filter = Mock()
        self.organizer = PhotoOrganizer(
            self.mock_date_extractor,
            self.mock_file_filter
        )
    
    @patch('main_improved.PathValidator.validate_source_path')
    @patch.object(PhotoOrganizer, '_get_files_to_process')
    def test_organize_no_files(self, mock_get_files, mock_validate):
        mock_validate.return_value = Path("/test/path")
        mock_get_files.return_value = []
        
        # Should not raise any exception
        self.organizer.organize("/test/path", dry_run=True)
    
    @patch('main_improved.PathValidator.validate_source_path')
    @patch.object(PhotoOrganizer, '_get_files_to_process')
    @patch.object(PhotoOrganizer, '_process_file')
    def test_organize_with_files(self, mock_process, mock_get_files, mock_validate):
        mock_validate.return_value = Path("/test/path")
        mock_files = [Path("/test/file1.jpg"), Path("/test/file2.jpg")]
        mock_get_files.return_value = mock_files
        
        self.organizer.organize("/test/path", dry_run=True)
        
        self.assertEqual(mock_process.call_count, 2)


if __name__ == '__main__':
    unittest.main()
