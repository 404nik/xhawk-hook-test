import hashlib
import time
import uuid
from typing import Dict, List, Optional

from .storage import VideoBlobStorage
from .manifest import VideoManifest
from .transcode import Transcoder


class StreamingServer:
    """
    Main streaming server combining storage, manifest, and transcoding.
    """

    def __init__(self, storage_root: str = None, manifest_path: str = None):
        """
        Initialize StreamingServer.
        
        Args:
            storage_root: Root directory for video storage
            manifest_path: Path to manifest JSON file
        """
        self.storage = VideoBlobStorage(root_dir=storage_root)
        self.manifest = VideoManifest(manifest_path=manifest_path)
        self.transcoder = Transcoder()

    def upload(
        self,
        uploader: str,
        title: str,
        data: bytes,
        mime_type: str,
        duration_sec: float
    ) -> str:
        """
        Upload a video.
        
        Args:
            uploader: Uploader name
            title: Video title
            data: Video data as bytes
            mime_type: MIME type (e.g., "video/mp4")
            duration_sec: Duration in seconds
            
        Returns:
            video_id for the uploaded video
        """
        # Generate unique video_id
        video_id = str(uuid.uuid4())
        
        # Store video data
        self.storage.put_video(video_id, data)
        
        # Register metadata
        metadata = {
            'title': title,
            'duration_sec': duration_sec,
            'mime_type': mime_type,
            'size_bytes': len(data),
            'uploader': uploader,
            'upload_ts': time.time()
        }
        self.manifest.register(video_id, metadata)
        
        return video_id

    def stream(self, video_id: str, range_start: int = 0, range_end: Optional[int] = None) -> bytes:
        """
        Stream video data with HTTP-range-style partial reads.
        
        Args:
            video_id: Video identifier
            range_start: Start byte (inclusive)
            range_end: End byte (inclusive), None means to end of file
            
        Returns:
            Video data bytes for the requested range
            
        Raises:
            FileNotFoundError: If video does not exist
        """
        data = self.storage.get_video(video_id)
        
        # Handle range requests
        if range_end is None:
            range_end = len(data) - 1
        
        # Clamp to valid range
        range_start = max(0, range_start)
        range_end = min(len(data) - 1, range_end)
        
        # Return empty if invalid range
        if range_start > range_end or range_start >= len(data):
            return b''
        
        return data[range_start:range_end + 1]

    def search(self, query: str) -> List[Dict]:
        """
        Search videos by title substring.
        
        Args:
            query: Search query (substring)
            
        Returns:
            List of matching video metadata dicts
        """
        return self.manifest.search_title(query)

    def request_transcode(self, video_id: str, quality: str) -> str:
        """
        Request transcoding of a video.
        
        Args:
            video_id: Source video identifier
            quality: Target quality string
            
        Returns:
            Transcoded video_id
        """
        # Get the transcoded video_id
        transcoded_id = self.transcoder.transcode(video_id, quality)
        
        # Generate deterministic transcoded data
        original_data = self.storage.get_video(video_id)
        combined = f"{video_id}:{quality}".encode()
        derived_bytes = hashlib.sha256(combined + original_data).digest()
        
        # Store the transcoded video
        self.storage.put_video(transcoded_id, derived_bytes)
        
        # Register metadata for transcoded video
        original_metadata = self.manifest.lookup(video_id)
        if original_metadata:
            transcoded_metadata = original_metadata.copy()
            transcoded_metadata['title'] = f"{original_metadata['title']} ({quality})"
            transcoded_metadata['size_bytes'] = len(derived_bytes)
            transcoded_metadata['upload_ts'] = time.time()
            self.manifest.register(transcoded_id, transcoded_metadata)
        
        return transcoded_id

    def list_by_uploader(self, uploader: str) -> List[Dict]:
        """
        List all videos by a specific uploader.
        
        Args:
            uploader: Uploader name
            
        Returns:
            List of video metadata dicts
        """
        return self.manifest.list_by_uploader(uploader)

    def delete(self, video_id: str) -> None:
        """
        Delete a video.
        
        Args:
            video_id: Video identifier
        """
        self.storage.delete_video(video_id)
        self.manifest.delete(video_id)
