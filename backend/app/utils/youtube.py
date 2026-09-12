"""YouTube utilities: URL validation and video ID extraction"""

import re
from typing import Optional, Tuple


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    
    Supported formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - URLs with additional parameters (t, list, index, etc.)
    
    Args:
        url: YouTube URL
        
    Returns:
        Video ID or None if not a valid YouTube URL
    """
    if not url or not isinstance(url, str):
        return None
    
    url = url.strip()
    
    # Pattern 1: youtu.be/VIDEO_ID or youtu.be/VIDEO_ID?t=...
    pattern1 = r'(?:https?://)?(?:www\.)?youtu\.be/([^/?&]+)'
    match = re.search(pattern1, url)
    if match:
        return match.group(1)
    
    # Pattern 2: youtube.com/watch?v=VIDEO_ID
    pattern2 = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([^&]+)'
    match = re.search(pattern2, url)
    if match:
        return match.group(1)
    
    # Pattern 3: youtube.com/shorts/VIDEO_ID
    pattern3 = r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([^/?&]+)'
    match = re.search(pattern3, url)
    if match:
        return match.group(1)
    
    return None


def is_valid_youtube_url(url: str) -> bool:
    """
    Check if URL is a valid YouTube URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid YouTube URL
    """
    if not url or not isinstance(url, str):
        return False
    
    # Check if it starts with http or https (or is protocol-relative)
    if not re.match(r'^https?://', url.strip()):
        return False
    
    # Check if it's a YouTube domain
    if not re.search(r'(youtube\.com|youtu\.be)', url):
        return False
    
    # Try to extract video ID
    video_id = extract_video_id(url)
    if not video_id:
        return False
    
    return validate_video_id(video_id)


def validate_video_id(video_id: str) -> bool:
    """
    Validate if a string is a valid YouTube video ID format.
    
    Args:
        video_id: Video ID to validate
        
    Returns:
        True if valid format
    """
    if not video_id or not isinstance(video_id, str):
        return False
    
    # YouTube video IDs are 11 characters, alphanumeric, dash, underscore
    return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))
