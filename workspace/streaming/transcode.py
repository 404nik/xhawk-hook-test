import hashlib
import uuid
from typing import Dict, Optional


class Transcoder:
    """
    Handles video transcoding (deterministic for this implementation).
    Tracks parent->derived video_id mappings.
    """

    def __init__(self):
        """Initialize Transcoder."""
        # Maps parent_video_id -> {quality -> derived_video_id}
        self._transcode_map: Dict[str, Dict[str, str]] = {}

    def transcode(self, video_id: str, target_quality: str) -> str:
        """
        Transcode a video to a target quality.
        
        For this implementation, "transcoding" generates deterministic derived bytes
        using sha256(input + quality) and creates a new video_id.
        
        Args:
            video_id: Source video identifier
            target_quality: Target quality string (e.g., "720p", "480p")
            
        Returns:
            New video_id for the transcoded video
        """
        # Check if we already have this transcode
        if video_id in self._transcode_map:
            if target_quality in self._transcode_map[video_id]:
                return self._transcode_map[video_id][target_quality]
        
        # Generate deterministic derived video_id
        # Use sha256(video_id + quality) to create a deterministic output
        combined = f"{video_id}:{target_quality}".encode()
        derived_hash = hashlib.sha256(combined).hexdigest()
        derived_video_id = f"{video_id}__{target_quality}__{derived_hash[:16]}"
        
        # Track the mapping
        if video_id not in self._transcode_map:
            self._transcode_map[video_id] = {}
        self._transcode_map[video_id][target_quality] = derived_video_id
        
        return derived_video_id

    def get_parent(self, derived_video_id: str) -> Optional[str]:
        """
        Get the parent video_id of a derived video.
        
        Args:
            derived_video_id: Derived video identifier
            
        Returns:
            Parent video_id or None if not a derived video
        """
        for parent_id, qualities in self._transcode_map.items():
            for quality, derived_id in qualities.items():
                if derived_id == derived_video_id:
                    return parent_id
        return None

    def get_transcode_quality(self, derived_video_id: str) -> Optional[str]:
        """
        Get the quality of a derived video.
        
        Args:
            derived_video_id: Derived video identifier
            
        Returns:
            Quality string or None if not a derived video
        """
        for parent_id, qualities in self._transcode_map.items():
            for quality, derived_id in qualities.items():
                if derived_id == derived_video_id:
                    return quality
        return None
