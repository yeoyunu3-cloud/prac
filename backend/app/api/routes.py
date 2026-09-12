"""API routes"""

import os
import logging
from fastapi import APIRouter, HTTPException, Query
from app.schemas.models import (
    VideoInfoResponse,
    SummarizeRequest,
    SummarizeResponse,
    ErrorResponse,
)
from app.services import get_video_info, get_transcript, split_transcript_into_chunks, get_available_languages, summarize_transcript
from app.utils.youtube import extract_video_id, is_valid_youtube_url


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "YouTube Lecture Summarizer API"
    }


@router.post("/video/info", response_model=VideoInfoResponse)
async def get_video_metadata(url: str = Query(..., description="YouTube URL")):
    """
    Get video information from URL.
    
    Supports multiple URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    
    try:
        # Validate URL
        if not is_valid_youtube_url(url):
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL format"
            )
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            raise HTTPException(
                status_code=400,
                detail="Could not extract video ID from URL"
            )
        
        # Get video info
        video_info = await get_video_info(video_id)
        
        # Get available languages
        try:
            available_languages = get_available_languages(video_id)
        except Exception as e:
            logger.warning(f"Could not fetch available languages: {str(e)}")
            available_languages = []
        
        return VideoInfoResponse(
            video_id=video_id,
            title=video_info["title"],
            channel=video_info["channel"],
            thumbnail_url=video_info["thumbnail_url"],
            available_languages=available_languages,
            original_url=url
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in get_video_info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch video information"
        )


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_video(request: SummarizeRequest):
    """
    Summarize a YouTube video.
    
    Process:
    1. Validate URL and extract video ID
    2. Fetch video metadata
    3. Get transcript in requested language
    4. Split transcript into chunks if needed
    5. Summarize using Claude API
    6. Return structured summary
    """
    
    try:
        # Validate URL
        if not is_valid_youtube_url(request.url):
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL format"
            )
        
        # Extract video ID
        video_id = extract_video_id(request.url)
        if not video_id:
            raise HTTPException(
                status_code=400,
                detail="Could not extract video ID from URL"
            )
        
        # Get video info
        video_info = await get_video_info(video_id)
        
        # Get transcript
        try:
            transcript_data, actual_language = get_transcript(
                video_id,
                language=request.transcript_language
            )
        except Exception as e:
            error_msg = str(e).lower()
            
            if "transcripts" in error_msg and "disabled" in error_msg:
                raise HTTPException(
                    status_code=400,
                    detail="This video has disabled transcripts/captions"
                )
            elif "no transcript" in error_msg or "not found" in error_msg:
                raise HTTPException(
                    status_code=400,
                    detail=f"No subtitles found for this video in the requested language ({request.transcript_language})"
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Could not fetch transcript for this video"
                )
        
        # Combine transcript segments
        full_transcript = " ".join([seg["text"] for seg in transcript_data])
        
        # Check transcript length and split if needed
        if len(full_transcript) > 10000:
            chunks = split_transcript_into_chunks(transcript_data, max_chunk_length=2000)
        else:
            chunks = split_transcript_into_chunks(transcript_data)
        
        # Get Anthropic API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not set")
            raise HTTPException(
                status_code=500,
                detail="API configuration error"
            )
        
        # Get model name
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        
        # Summarize transcript
        summary = await summarize_transcript(
            full_transcript,
            detail_level=request.detail_level,
            output_language=request.output_language,
            model=model,
            api_key=api_key
        )
        
        return SummarizeResponse(
            video_id=video_id,
            title=video_info["title"],
            channel=video_info["channel"],
            thumbnail_url=video_info["thumbnail_url"],
            summary=summary,
            transcript_language=actual_language,
            output_language=request.output_language
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in summarize_video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to summarize video. Please try again."
        )


@router.get("/video/languages")
async def get_video_languages(url: str = Query(..., description="YouTube URL")):
    """Get available transcript languages for a video"""
    
    try:
        if not is_valid_youtube_url(url):
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL"
            )
        
        video_id = extract_video_id(url)
        if not video_id:
            raise HTTPException(
                status_code=400,
                detail="Could not extract video ID"
            )
        
        languages = get_available_languages(video_id)
        
        return {
            "video_id": video_id,
            "languages": languages
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting languages: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch available languages"
        )
