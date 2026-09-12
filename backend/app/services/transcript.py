"""Transcript handling and chunking"""

import json
from typing import List, Dict, Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class TranscriptSegment:
    """Represents a single segment of transcript"""
    
    def __init__(self, text: str, start: float, duration: float):
        self.text = text
        self.start = start
        self.duration = duration
        self.end = start + duration
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "start": self.start,
            "duration": self.duration
        }


class TranscriptChunk:
    """Represents a chunk of transcript segments"""
    
    def __init__(self, segments: List[TranscriptSegment], chunk_index: int):
        self.segments = segments
        self.chunk_index = chunk_index
        self.full_text = " ".join(seg.text for seg in segments)
        self.start_time = segments[0].start if segments else 0
        self.end_time = segments[-1].end if segments else 0
    
    def to_dict(self) -> Dict:
        return {
            "chunk_index": self.chunk_index,
            "text": self.full_text,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "segments": [seg.to_dict() for seg in self.segments]
        }


def get_transcript(video_id: str, language: str = "ko") -> Tuple[List[Dict], str]:
    """
    Fetch transcript from YouTube video.
    
    Language preference order:
    1. User-selected language
    2. Korean (manual)
    3. English (manual)
    4. Korean (auto)
    5. English (auto)
    6. First available
    
    Args:
        video_id: YouTube video ID
        language: Preferred language code (e.g., 'ko', 'en')
        
    Returns:
        Tuple of (transcript list, actual language used)
        
    Raises:
        TranscriptsDisabled: If transcripts are disabled
        NoTranscriptFound: If no transcript available
    """
    try:
        # Get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except TranscriptsDisabled:
        raise TranscriptsDisabled(video_id)
    except Exception as e:
        raise NoTranscriptFound(
            video_id=video_id, 
            requested_language=language,
            available_languages=[],
            caused_by=e
        )
    
    # Try to get transcript in order of preference
    candidates = []
    
    # 1. User-selected language (manual first)
    if hasattr(transcript_list, 'find_transcript') and language:
        try:
            transcript = transcript_list.find_transcript([language])
            candidates.append((transcript, language, True))
        except Exception:
            pass
    
    # 2. Korean (manual)
    if hasattr(transcript_list, 'find_transcript'):
        try:
            transcript = transcript_list.find_transcript(['ko'])
            candidates.append((transcript, 'ko', True))
        except Exception:
            pass
    
    # 3. English (manual)
    if hasattr(transcript_list, 'find_transcript'):
        try:
            transcript = transcript_list.find_transcript(['en'])
            candidates.append((transcript, 'en', True))
        except Exception:
            pass
    
    # 4. Manual transcripts
    for transcript in transcript_list.manually_created_transcripts:
        candidates.append((transcript, transcript.language, True))
    
    # 5. Auto-generated transcripts
    for transcript in transcript_list.generated_transcripts:
        candidates.append((transcript, transcript.language, False))
    
    if not candidates:
        available = []
        if hasattr(transcript_list, 'manually_created_transcripts'):
            available.extend([t.language for t in transcript_list.manually_created_transcripts])
        if hasattr(transcript_list, 'generated_transcripts'):
            available.extend([t.language for t in transcript_list.generated_transcripts])
        
        raise NoTranscriptFound(
            video_id=video_id,
            requested_language=language,
            available_languages=available
        )
    
    # Fetch the first available transcript
    transcript, actual_language, is_manual = candidates[0]
    transcript_data = transcript.fetch()
    
    return transcript_data, actual_language


def split_transcript_into_chunks(
    segments: List[Dict],
    max_chunk_length: int = 2000
) -> List[TranscriptChunk]:
    """
    Split transcript segments into chunks while respecting boundaries.
    
    Args:
        segments: List of transcript segments with 'text', 'start', 'duration'
        max_chunk_length: Maximum characters per chunk
        
    Returns:
        List of TranscriptChunk objects
    """
    if not segments:
        return []
    
    # Convert to TranscriptSegment objects
    segment_objects = [
        TranscriptSegment(seg['text'], seg['start'], seg.get('duration', 0))
        for seg in segments
    ]
    
    chunks = []
    current_chunk_segments = []
    current_length = 0
    chunk_index = 0
    
    for segment in segment_objects:
        segment_length = len(segment.text)
        
        # If adding this segment exceeds max length and we have content
        if current_length + segment_length > max_chunk_length and current_chunk_segments:
            # Save current chunk
            chunks.append(TranscriptChunk(current_chunk_segments, chunk_index))
            chunk_index += 1
            current_chunk_segments = []
            current_length = 0
        
        # Add segment to current chunk
        current_chunk_segments.append(segment)
        current_length += segment_length + 1  # +1 for space
    
    # Don't forget the last chunk
    if current_chunk_segments:
        chunks.append(TranscriptChunk(current_chunk_segments, chunk_index))
    
    return chunks


def get_available_languages(video_id: str) -> List[str]:
    """
    Get list of available transcript languages for a video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        List of language codes
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = []
        
        for transcript in transcript_list.manually_created_transcripts:
            languages.append(transcript.language)
        
        for transcript in transcript_list.generated_transcripts:
            languages.append(transcript.language)
        
        return list(set(languages))  # Remove duplicates
    except Exception:
        return []
