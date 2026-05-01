import json
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Optional


class VideoManifest:
    """
    Tracks video metadata with persistent JSON storage.
    """

    def __init__(self, manifest_path: str = None):
        """
        Initialize VideoManifest.
        
        Args:
            manifest_path: Path to JSON manifest file. Defaults to a temp file.
        """
        if manifest_path is None:
            # Create a temp directory and use a manifest file in it
            self.temp_dir = tempfile.mkdtemp(prefix="video_manifest_")
            manifest_path = os.path.join(self.temp_dir, "manifest.json")
        else:
            self.temp_dir = None
        
        self.manifest_path = Path(manifest_path)
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Dict] = {}
        self._load()

    def _load(self) -> None:
        """Load manifest from disk."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                self._data = json.load(f)
        else:
            self._data = {}

    def _save(self) -> None:
        """Save manifest to disk atomically."""
        # Write to temporary file first
        temp_fd, temp_path = tempfile.mkstemp(dir=self.manifest_path.parent)
        try:
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(self._data, f, indent=2)
            # Atomic rename
            os.replace(temp_path, self.manifest_path)
        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def register(self, video_id: str, metadata: Dict) -> None:
        """
        Register a video with metadata.
        
        Args:
            video_id: Unique video identifier
            metadata: Dict with keys: title, duration_sec, mime_type, size_bytes, uploader, upload_ts
        """
        self._data[video_id] = metadata
        self._save()

    def lookup(self, video_id: str) -> Optional[Dict]:
        """
        Look up video metadata.
        
        Args:
            video_id: Unique video identifier
            
        Returns:
            Metadata dict or None if not found
        """
        return self._data.get(video_id)

    def list_by_uploader(self, uploader: str) -> List[Dict]:
        """
        List all videos by a specific uploader.
        
        Args:
            uploader: Uploader name
            
        Returns:
            List of metadata dicts
        """
        return [
            metadata for metadata in self._data.values()
            if metadata.get('uploader') == uploader
        ]

    def search_title(self, substring: str) -> List[Dict]:
        """
        Search videos by title substring (case-insensitive).
        
        Args:
            substring: Search substring
            
        Returns:
            List of metadata dicts matching the substring
        """
        substring_lower = substring.lower()
        return [
            metadata for metadata in self._data.values()
            if substring_lower in metadata.get('title', '').lower()
        ]

    def delete(self, video_id: str) -> None:
        """
        Delete a video from the manifest.
        
        Args:
            video_id: Unique video identifier
        """
        if video_id in self._data:
            del self._data[video_id]
            self._save()

    def list_all(self) -> List[Dict]:
        """
        List all videos.
        
        Returns:
            List of all metadata dicts
        """
        return list(self._data.values())
