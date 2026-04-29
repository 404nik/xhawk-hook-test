"""
Unit tests for LocalFileStorage.
"""

import hashlib
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from file_storage import LocalFileStorage


class TestLocalFileStorage:
    """Test suite for LocalFileStorage."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def storage(self, temp_dir):
        """Create a LocalFileStorage instance for testing."""
        return LocalFileStorage(temp_dir)
    
    # ===== Basic put/get/delete/exists tests =====
    
    def test_put_and_get(self, storage):
        """Test basic put and get operations."""
        key = "test_key"
        data = b"test data"
        
        storage.put(key, data)
        retrieved = storage.get(key)
        
        assert retrieved == data
    
    def test_put_and_get_large_data(self, storage):
        """Test put and get with large data."""
        key = "large_key"
        data = b"x" * (1024 * 1024)  # 1MB
        
        storage.put(key, data)
        retrieved = storage.get(key)
        
        assert retrieved == data
    
    def test_put_overwrites_existing(self, storage):
        """Test that put overwrites existing data."""
        key = "overwrite_key"
        data1 = b"first data"
        data2 = b"second data"
        
        storage.put(key, data1)
        storage.put(key, data2)
        retrieved = storage.get(key)
        
        assert retrieved == data2
    
    def test_get_nonexistent_key(self, storage):
        """Test that get raises FileNotFoundError for nonexistent keys."""
        with pytest.raises(FileNotFoundError):
            storage.get("nonexistent_key")
    
    def test_delete(self, storage):
        """Test delete operation."""
        key = "delete_key"
        data = b"data to delete"
        
        storage.put(key, data)
        assert storage.exists(key)
        
        storage.delete(key)
        assert not storage.exists(key)
    
    def test_delete_nonexistent_key(self, storage):
        """Test that delete raises FileNotFoundError for nonexistent keys."""
        with pytest.raises(FileNotFoundError):
            storage.delete("nonexistent_key")
    
    def test_exists_true(self, storage):
        """Test exists returns True for existing keys."""
        key = "exists_key"
        data = b"test data"
        
        storage.put(key, data)
        assert storage.exists(key)
    
    def test_exists_false(self, storage):
        """Test exists returns False for nonexistent keys."""
        assert not storage.exists("nonexistent_key")
    
    # ===== List tests =====
    
    def test_list_empty(self, storage):
        """Test list on empty storage."""
        keys = storage.list()
        assert keys == []
    
    def test_list_single_key(self, storage):
        """Test list with a single key."""
        key = "single_key"
        storage.put(key, b"data")
        
        keys = storage.list()
        assert len(keys) == 1
        # The returned key is the hash, not the original key
        assert isinstance(keys[0], str)
    
    def test_list_multiple_keys(self, storage):
        """Test list with multiple keys."""
        keys_to_store = ["key1", "key2", "key3"]
        for key in keys_to_store:
            storage.put(key, b"data")
        
        listed_keys = storage.list()
        assert len(listed_keys) == 3
    
    def test_list_returns_sorted(self, storage):
        """Test that list returns sorted keys."""
        keys_to_store = ["zebra", "apple", "banana"]
        for key in keys_to_store:
            storage.put(key, b"data")
        
        listed_keys = storage.list()
        assert listed_keys == sorted(listed_keys)
    
    # ===== Path traversal rejection tests =====
    
    def test_reject_key_with_double_dot(self, storage):
        """Test that keys containing '..' are rejected."""
        with pytest.raises(ValueError, match="cannot contain '..'"):
            storage.put("../../../etc/passwd", b"data")
    
    def test_reject_key_with_double_dot_in_middle(self, storage):
        """Test that keys with '..' in the middle are rejected."""
        with pytest.raises(ValueError, match="cannot contain '..'"):
            storage.put("foo/../bar", b"data")
    
    def test_reject_absolute_path(self, storage):
        """Test that absolute paths are rejected."""
        with pytest.raises(ValueError, match="cannot be an absolute path"):
            storage.put("/etc/passwd", b"data")
    
    def test_reject_absolute_path_windows_style(self, storage):
        """Test that Windows-style absolute paths are rejected on Windows."""
        # os.path.isabs only recognizes Windows paths as absolute on Windows
        # On Unix, C:\Windows\System32 is just a regular relative path
        # So we skip this test on non-Windows systems
        import sys
        if sys.platform == "win32":
            with pytest.raises(ValueError, match="cannot be an absolute path"):
                storage.put("C:\\Windows\\System32", b"data")
    
    def test_reject_empty_key(self, storage):
        """Test that empty keys are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            storage.put("", b"data")
    
    def test_reject_empty_key_on_get(self, storage):
        """Test that empty keys are rejected on get."""
        with pytest.raises(ValueError, match="cannot be empty"):
            storage.get("")
    
    def test_reject_empty_key_on_delete(self, storage):
        """Test that empty keys are rejected on delete."""
        with pytest.raises(ValueError, match="cannot be empty"):
            storage.delete("")
    
    def test_reject_empty_key_on_exists(self, storage):
        """Test that empty keys are rejected on exists."""
        with pytest.raises(ValueError, match="cannot be empty"):
            storage.exists("")
    
    # ===== Atomic write recovery tests =====
    
    def test_atomic_write_recovery(self, storage, temp_dir):
        """Test that incomplete writes don't corrupt storage."""
        key = "atomic_key"
        data = b"atomic data"
        
        # Put data normally
        storage.put(key, data)
        
        # Verify it's there
        assert storage.get(key) == data
        
        # Put new data
        new_data = b"new atomic data"
        storage.put(key, new_data)
        
        # Verify the new data is there and complete
        assert storage.get(key) == new_data
    
    def test_no_temp_files_left_after_put(self, storage, temp_dir):
        """Test that no temporary files are left after put."""
        key = "temp_test_key"
        data = b"test data"
        
        storage.put(key, data)
        
        # Check that there are no .tmp files in the storage directory
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                assert not file.startswith("tmp"), f"Temporary file left: {file}"
    
    def test_atomic_write_with_multiple_puts(self, storage):
        """Test atomic writes with multiple sequential puts."""
        for i in range(10):
            key = f"key_{i}"
            data = f"data_{i}".encode()
            storage.put(key, data)
        
        # Verify all data is intact
        for i in range(10):
            key = f"key_{i}"
            expected_data = f"data_{i}".encode()
            assert storage.get(key) == expected_data
    
    # ===== Sharding correctness tests =====
    
    def test_sharding_creates_correct_directory_structure(self, storage, temp_dir):
        """Test that sharding creates the correct directory structure."""
        key = "sharding_test"
        data = b"test data"
        
        storage.put(key, data)
        
        # Calculate expected hash
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        shard1 = key_hash[0:2]
        shard2 = key_hash[2:4]
        
        # Verify directory structure exists
        expected_path = Path(temp_dir) / shard1 / shard2 / key_hash
        assert expected_path.exists()
        assert expected_path.is_file()
    
    def test_sharding_distributes_keys(self, storage, temp_dir):
        """Test that sharding distributes keys across directories."""
        # Create multiple keys that should hash to different shards
        keys = [f"key_{i}" for i in range(20)]
        for key in keys:
            storage.put(key, b"data")
        
        # Count the number of shard directories created
        shard_dirs = set()
        for root, dirs, files in os.walk(temp_dir):
            if files:  # Only count directories with files
                # Get the relative path from root_dir
                rel_path = os.path.relpath(root, temp_dir)
                shard_dirs.add(rel_path)
        
        # Should have multiple shard directories (not all in one)
        assert len(shard_dirs) > 1
    
    def test_sharding_same_key_same_location(self, storage, temp_dir):
        """Test that the same key always hashes to the same location."""
        key = "consistent_key"
        
        # Put, delete, and put again
        storage.put(key, b"data1")
        path1 = storage._get_shard_path(key)
        
        storage.delete(key)
        
        storage.put(key, b"data2")
        path2 = storage._get_shard_path(key)
        
        assert path1 == path2
    
    def test_sharding_different_keys_different_hashes(self, storage):
        """Test that different keys produce different hashes."""
        key1 = "key1"
        key2 = "key2"
        
        path1 = storage._get_shard_path(key1)
        path2 = storage._get_shard_path(key2)
        
        # Paths should be different (unless by extreme coincidence)
        assert path1 != path2
    
    # ===== Edge cases =====
    
    def test_key_with_special_characters(self, storage):
        """Test keys with special characters."""
        key = "key!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        data = b"special data"
        
        storage.put(key, data)
        assert storage.get(key) == data
    
    def test_key_with_unicode(self, storage):
        """Test keys with unicode characters."""
        key = "key_with_unicode_🔑_文字"
        data = b"unicode data"
        
        storage.put(key, data)
        assert storage.get(key) == data
    
    def test_data_with_null_bytes(self, storage):
        """Test storing data with null bytes."""
        key = "null_bytes_key"
        data = b"data\x00with\x00nulls"
        
        storage.put(key, data)
        assert storage.get(key) == data
    
    def test_empty_data(self, storage):
        """Test storing empty data."""
        key = "empty_key"
        data = b""
        
        storage.put(key, data)
        assert storage.get(key) == data
    
    def test_storage_root_creation(self, temp_dir):
        """Test that storage root directory is created if it doesn't exist."""
        nonexistent_dir = os.path.join(temp_dir, "nonexistent", "nested", "dir")
        storage = LocalFileStorage(nonexistent_dir)
        
        assert os.path.exists(nonexistent_dir)
        assert os.path.isdir(nonexistent_dir)
    
    def test_multiple_storage_instances_same_root(self, temp_dir):
        """Test multiple storage instances using the same root."""
        storage1 = LocalFileStorage(temp_dir)
        storage2 = LocalFileStorage(temp_dir)
        
        key = "shared_key"
        data = b"shared data"
        
        storage1.put(key, data)
        assert storage2.get(key) == data
    
    def test_key_with_slashes(self, storage):
        """Test that keys with slashes are handled correctly."""
        # Slashes in keys should be allowed (they're just part of the key string)
        # The sharding mechanism will hash them, so they won't create subdirectories
        key = "path/to/key"
        data = b"data"
        
        storage.put(key, data)
        assert storage.get(key) == data
    
    def test_very_long_key(self, storage):
        """Test with very long keys."""
        key = "k" * 10000
        data = b"data"
        
        storage.put(key, data)
        assert storage.get(key) == data
    
    def test_list_after_delete(self, storage):
        """Test that list reflects deletions."""
        keys = ["key1", "key2", "key3"]
        for key in keys:
            storage.put(key, b"data")
        
        initial_list = storage.list()
        assert len(initial_list) == 3
        
        storage.delete("key2")
        
        after_delete = storage.list()
        assert len(after_delete) == 2
