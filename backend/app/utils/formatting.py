"""Timestamp and formatting utilities"""


def seconds_to_timestamp(seconds: int) -> str:
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Total seconds
        
    Returns:
        Formatted timestamp string
    """
    if seconds < 0:
        seconds = 0
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def timestamp_to_seconds(timestamp: str) -> int:
    """
    Convert timestamp (MM:SS or HH:MM:SS) to seconds.
    
    Args:
        timestamp: Formatted timestamp
        
    Returns:
        Total seconds
    """
    parts = timestamp.split(":")
    
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    
    return 0


def build_youtube_timestamp_url(video_id: str, seconds: int) -> str:
    """
    Build YouTube URL with timestamp.
    
    Args:
        video_id: YouTube video ID
        seconds: Timestamp in seconds
        
    Returns:
        YouTube URL with timestamp
    """
    return f"https://www.youtube.com/watch?v={video_id}&t={seconds}s"
