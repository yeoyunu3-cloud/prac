"""YouTube video information service"""

import httpx
from typing import Dict, Optional


async def get_video_info(video_id: str) -> Dict:
    """
    Fetch video information using YouTube oEmbed API.
    
    No API key required - uses public oEmbed endpoint.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with title, channel, thumbnail, etc.
        
    Raises:
        Exception: If video not found or API error
    """
    
    url = "https://www.youtube.com/oembed"
    params = {
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "format": "json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "title": data.get("title", "Unknown"),
                "channel": data.get("author_name", "Unknown"),
                "thumbnail_url": data.get("thumbnail_url", ""),
                "width": data.get("width"),
                "height": data.get("height")
            }
    
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Video not found: {video_id}")
        else:
            raise Exception(f"Failed to fetch video info: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching video information: {str(e)}")
