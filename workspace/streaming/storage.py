import hashlib
import os
import tempfile
from pathlib import Path


class VideoBlobStorage:
    """
    Stores video blobs with sharding based on sha256 hash.
    Sharding structure: sha256(video_id)[0:2]/[2:4]/<full-hash>
    """

    def __init__(self, root_dir: str = None):
        """
        Initialize VideoBlobStorage.
        
        Args:
            root_dir: Root directory for storing videos. Defaults to a temp directory.
        """
        if root_dir is None:
            root_dir = tempfile.mkdtemp(prefix="video_storage_")
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def _get_shard_path(self, video_id: str) -> Path:
        """
        Get the shard path for a video_id using sha256 hash.
        
        Returns: Path object for the video file
        """
        hash_hex = hashlib.sha256(video_id.encode()).hexdigest()
        shard1 = hash_hex[0:2]
        shard2 = hash_hex[2:4]
        shard_dir = self.root_dir / shard1 / shard2
        shard_dir.mkdir(parents=True, exist_ok=True)
        return shard_dir / hash_hex

    def put_video(self, video_id: str, data: bytes) -> None:
        """
        Store video data atomically.
        
        Args:
            video_id: Unique video identifier
            data: Video data as bytes
        """
        video_path = self._get_shard_path(video_id)
        
        # Write to temporary file first
        temp_fd, temp_path = tempfile.mkstemp(dir=video_path.parent)
        try:
            with os.fdopen(temp_fd, 'wb') as f:
                f.write(data)
            # Atomic rename
            os.replace(temp_path, video_path)
        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def get_video(self, video_id: str) -> bytes:
        """
        Retrieve video data.
        
        Args:
            video_id: Unique video identifier
            
        Returns:
            Video data as bytes
            
        Raises:
            FileNotFoundError: If video does not exist
        """
        video_path = self._get_shard_path(video_id)
        if not video_path.exists():
            raise FileNotFoundError(f"Video {video_id} not found")
        
        with open(video_path, 'rb') as f:
            return f.read()

    def has_video(self, video_id: str) -> bool:
        """
        Check if a video exists.
        
        Args:
            video_id: Unique video identifier
            
        Returns:
            True if video exists, False otherwise
        """
        video_path = self._get_shard_path(video_id)
        return video_path.exists()

    def delete_video(self, video_id: str) -> None:
        """
        Delete a video.
        
        Args:
            video_id: Unique video identifier
        """
        video_path = self._get_shard_path(video_id)
        if video_path.exists():
            video_path.unlink()
