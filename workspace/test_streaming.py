import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

import pytest

from streaming import (
    VideoBlobStorage,
    VideoManifest,
    Transcoder,
    StreamingServer,
)


class TestVideoBlobStorage:
    """Test VideoBlobStorage class."""

    def test_put_and_get_video(self):
        """Test basic put and get operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "test_video_1"
            data = b"test video data"
            
            storage.put_video(video_id, data)
            retrieved = storage.get_video(video_id)
            
            assert retrieved == data

    def test_has_video(self):
        """Test has_video method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "test_video_2"
            
            assert not storage.has_video(video_id)
            
            storage.put_video(video_id, b"data")
            assert storage.has_video(video_id)

    def test_delete_video(self):
        """Test delete_video method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "test_video_3"
            
            storage.put_video(video_id, b"data")
            assert storage.has_video(video_id)
            
            storage.delete_video(video_id)
            assert not storage.has_video(video_id)

    def test_sharding_structure(self):
        """Test that sharding creates correct directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "test_video_4"
            data = b"test data"
            
            storage.put_video(video_id, data)
            
            # Verify sharding structure
            hash_hex = hashlib.sha256(video_id.encode()).hexdigest()
            shard1 = hash_hex[0:2]
            shard2 = hash_hex[2:4]
            
            expected_path = Path(tmpdir) / shard1 / shard2 / hash_hex
            assert expected_path.exists()

    def test_atomic_write(self):
        """Test that writes are atomic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "test_video_5"
            data = b"test data for atomic write"
            
            storage.put_video(video_id, data)
            
            # Verify no .tmp files are left
            tmp_files = list(Path(tmpdir).rglob("*.tmp"))
            assert len(tmp_files) == 0

    def test_get_nonexistent_video(self):
        """Test getting a nonexistent video raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            
            with pytest.raises(FileNotFoundError):
                storage.get_video("nonexistent")

    def test_empty_bytes(self):
        """Test storing and retrieving empty bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "empty_video"
            data = b""
            
            storage.put_video(video_id, data)
            retrieved = storage.get_video(video_id)
            
            assert retrieved == b""

    def test_large_bytes(self):
        """Test storing and retrieving large bytes (~1MB)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = VideoBlobStorage(root_dir=tmpdir)
            video_id = "large_video"
            data = b"x" * (1024 * 1024)  # 1MB
            
            storage.put_video(video_id, data)
            retrieved = storage.get_video(video_id)
            
            assert retrieved == data
            assert len(retrieved) == 1024 * 1024


class TestVideoManifest:
    """Test VideoManifest class."""

    def test_register_and_lookup(self):
        """Test register and lookup operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = VideoManifest(manifest_path=manifest_path)
            
            video_id = "video_1"
            metadata = {
                'title': 'Test Video',
                'duration_sec': 120.5,
                'mime_type': 'video/mp4',
                'size_bytes': 1024,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            
            manifest.register(video_id, metadata)
            retrieved = manifest.lookup(video_id)
            
            assert retrieved == metadata

    def test_lookup_nonexistent(self):
        """Test looking up nonexistent video returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = VideoManifest(manifest_path=manifest_path)
            
            assert manifest.lookup("nonexistent") is None

    def test_list_by_uploader(self):
        """Test listing videos by uploader."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = VideoManifest(manifest_path=manifest_path)
            
            metadata1 = {
                'title': 'Video 1',
                'duration_sec': 100,
                'mime_type': 'video/mp4',
                'size_bytes': 1024,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            metadata2 = {
                'title': 'Video 2',
                'duration_sec': 200,
                'mime_type': 'video/mp4',
                'size_bytes': 2048,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            metadata3 = {
                'title': 'Video 3',
                'duration_sec': 300,
                'mime_type': 'video/mp4',
                'size_bytes': 3072,
                'uploader': 'user2',
                'upload_ts': time.time()
            }
            
            manifest.register('video_1', metadata1)
            manifest.register('video_2', metadata2)
            manifest.register('video_3', metadata3)
            
            user1_videos = manifest.list_by_uploader('user1')
            assert len(user1_videos) == 2
            assert all(v['uploader'] == 'user1' for v in user1_videos)

    def test_search_title(self):
        """Test searching videos by title substring."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = VideoManifest(manifest_path=manifest_path)
            
            metadata1 = {
                'title': 'Python Tutorial',
                'duration_sec': 100,
                'mime_type': 'video/mp4',
                'size_bytes': 1024,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            metadata2 = {
                'title': 'JavaScript Guide',
                'duration_sec': 200,
                'mime_type': 'video/mp4',
                'size_bytes': 2048,
                'uploader': 'user2',
                'upload_ts': time.time()
            }
            metadata3 = {
                'title': 'Python Advanced',
                'duration_sec': 300,
                'mime_type': 'video/mp4',
                'size_bytes': 3072,
                'uploader': 'user3',
                'upload_ts': time.time()
            }
            
            manifest.register('video_1', metadata1)
            manifest.register('video_2', metadata2)
            manifest.register('video_3', metadata3)
            
            results = manifest.search_title('python')
            assert len(results) == 2
            assert all('python' in v['title'].lower() for v in results)

    def test_search_title_case_insensitive(self):
        """Test that title search is case-insensitive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = VideoManifest(manifest_path=manifest_path)
            
            metadata = {
                'title': 'Python Tutorial',
                'duration_sec': 100,
                'mime_type': 'video/mp4',
                'size_bytes': 1024,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            
            manifest.register('video_1', metadata)
            
            # Search with different cases
            assert len(manifest.search_title('PYTHON')) == 1
            assert len(manifest.search_title('python')) == 1
            assert len(manifest.search_title('PyThOn')) == 1

    def test_delete(self):
        """Test deleting a video from manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            manifest = VideoManifest(manifest_path=manifest_path)
            
            video_id = "video_1"
            metadata = {
                'title': 'Test Video',
                'duration_sec': 100,
                'mime_type': 'video/mp4',
                'size_bytes': 1024,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            
            manifest.register(video_id, metadata)
            assert manifest.lookup(video_id) is not None
            
            manifest.delete(video_id)
            assert manifest.lookup(video_id) is None

    def test_persistence_across_reloads(self):
        """Test that manifest persists across reloads."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            # Create and populate manifest
            manifest1 = VideoManifest(manifest_path=manifest_path)
            metadata = {
                'title': 'Test Video',
                'duration_sec': 100,
                'mime_type': 'video/mp4',
                'size_bytes': 1024,
                'uploader': 'user1',
                'upload_ts': time.time()
            }
            manifest1.register('video_1', metadata)
            
            # Reload manifest
            manifest2 = VideoManifest(manifest_path=manifest_path)
            retrieved = manifest2.lookup('video_1')
            
            assert retrieved == metadata


class TestTranscoder:
    """Test Transcoder class."""

    def test_transcode_deterministic(self):
        """Test that transcoding produces deterministic output."""
        transcoder = Transcoder()
        
        video_id = "video_1"
        quality = "720p"
        
        result1 = transcoder.transcode(video_id, quality)
        result2 = transcoder.transcode(video_id, quality)
        
        assert result1 == result2

    def test_transcode_different_qualities(self):
        """Test that different qualities produce different outputs."""
        transcoder = Transcoder()
        
        video_id = "video_1"
        
        result_720p = transcoder.transcode(video_id, "720p")
        result_480p = transcoder.transcode(video_id, "480p")
        
        assert result_720p != result_480p

    def test_get_parent(self):
        """Test getting parent video_id from derived video."""
        transcoder = Transcoder()
        
        video_id = "video_1"
        quality = "720p"
        
        derived_id = transcoder.transcode(video_id, quality)
        parent = transcoder.get_parent(derived_id)
        
        assert parent == video_id

    def test_get_transcode_quality(self):
        """Test getting quality from derived video."""
        transcoder = Transcoder()
        
        video_id = "video_1"
        quality = "720p"
        
        derived_id = transcoder.transcode(video_id, quality)
        retrieved_quality = transcoder.get_transcode_quality(derived_id)
        
        assert retrieved_quality == quality


class TestStreamingServer:
    """Test StreamingServer class."""

    def test_upload_and_stream_roundtrip(self):
        """Test upload and stream roundtrip."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            uploader = "user1"
            title = "Test Video"
            data = b"test video data"
            mime_type = "video/mp4"
            duration_sec = 120.5
            
            video_id = server.upload(uploader, title, data, mime_type, duration_sec)
            retrieved = server.stream(video_id)
            
            assert retrieved == data

    def test_stream_full_range(self):
        """Test streaming full video."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"0123456789"
            video_id = server.upload("user1", "Test", data, "video/mp4", 10)
            
            retrieved = server.stream(video_id, range_start=0, range_end=None)
            assert retrieved == data

    def test_stream_partial_range(self):
        """Test streaming partial video (mid-slice)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"0123456789"
            video_id = server.upload("user1", "Test", data, "video/mp4", 10)
            
            retrieved = server.stream(video_id, range_start=2, range_end=5)
            assert retrieved == b"2345"

    def test_stream_head_only(self):
        """Test streaming head-only (first byte)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"0123456789"
            video_id = server.upload("user1", "Test", data, "video/mp4", 10)
            
            retrieved = server.stream(video_id, range_start=0, range_end=0)
            assert retrieved == b"0"

    def test_stream_beyond_end(self):
        """Test streaming with range beyond file end."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"0123456789"
            video_id = server.upload("user1", "Test", data, "video/mp4", 10)
            
            # Request range beyond end
            retrieved = server.stream(video_id, range_start=5, range_end=100)
            assert retrieved == b"56789"

    def test_stream_invalid_range(self):
        """Test streaming with invalid range returns empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"0123456789"
            video_id = server.upload("user1", "Test", data, "video/mp4", 10)
            
            # Request range beyond file
            retrieved = server.stream(video_id, range_start=100, range_end=200)
            assert retrieved == b""

    def test_search_by_title(self):
        """Test searching videos by title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            server.upload("user1", "Python Tutorial", b"data1", "video/mp4", 100)
            server.upload("user2", "JavaScript Guide", b"data2", "video/mp4", 200)
            server.upload("user3", "Python Advanced", b"data3", "video/mp4", 300)
            
            results = server.search("python")
            assert len(results) == 2
            assert all('python' in v['title'].lower() for v in results)

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            server.upload("user1", "Python Tutorial", b"data", "video/mp4", 100)
            
            assert len(server.search("PYTHON")) == 1
            assert len(server.search("python")) == 1
            assert len(server.search("PyThOn")) == 1

    def test_request_transcode(self):
        """Test requesting transcode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"original video data"
            video_id = server.upload("user1", "Test Video", data, "video/mp4", 100)
            
            transcoded_id = server.request_transcode(video_id, "720p")
            
            assert transcoded_id != video_id
            assert server.storage.has_video(transcoded_id)

    def test_transcode_deterministic_output(self):
        """Test that transcoding produces deterministic output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"original video data"
            video_id = server.upload("user1", "Test Video", data, "video/mp4", 100)
            
            transcoded_id1 = server.request_transcode(video_id, "720p")
            transcoded_data1 = server.stream(transcoded_id1)
            
            # Request same transcode again
            transcoded_id2 = server.request_transcode(video_id, "720p")
            transcoded_data2 = server.stream(transcoded_id2)
            
            assert transcoded_id1 == transcoded_id2
            assert transcoded_data1 == transcoded_data2

    def test_list_by_uploader(self):
        """Test listing videos by uploader."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            server.upload("user1", "Video 1", b"data1", "video/mp4", 100)
            server.upload("user1", "Video 2", b"data2", "video/mp4", 200)
            server.upload("user2", "Video 3", b"data3", "video/mp4", 300)
            
            user1_videos = server.list_by_uploader("user1")
            assert len(user1_videos) == 2
            assert all(v['uploader'] == 'user1' for v in user1_videos)

    def test_missing_video_stream(self):
        """Test streaming nonexistent video raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            with pytest.raises(FileNotFoundError):
                server.stream("nonexistent")

    def test_empty_bytes_upload(self):
        """Test uploading empty bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            video_id = server.upload("user1", "Empty Video", b"", "video/mp4", 0)
            retrieved = server.stream(video_id)
            
            assert retrieved == b""

    def test_large_bytes_upload(self):
        """Test uploading large bytes (~1MB)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            data = b"x" * (1024 * 1024)  # 1MB
            video_id = server.upload("user1", "Large Video", data, "video/mp4", 100)
            retrieved = server.stream(video_id)
            
            assert retrieved == data
            assert len(retrieved) == 1024 * 1024

    def test_metadata_stored_correctly(self):
        """Test that metadata is stored correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_root = os.path.join(tmpdir, "storage")
            manifest_path = os.path.join(tmpdir, "manifest.json")
            
            server = StreamingServer(storage_root=storage_root, manifest_path=manifest_path)
            
            uploader = "user1"
            title = "Test Video"
            data = b"test data"
            mime_type = "video/mp4"
            duration_sec = 120.5
            
            video_id = server.upload(uploader, title, data, mime_type, duration_sec)
            metadata = server.manifest.lookup(video_id)
            
            assert metadata['title'] == title
            assert metadata['duration_sec'] == duration_sec
            assert metadata['mime_type'] == mime_type
            assert metadata['size_bytes'] == len(data)
            assert metadata['uploader'] == uploader
            assert 'upload_ts' in metadata
