"""Pydantic models for API requests and responses"""

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    """Difficulty levels"""
    BEGINNER = "입문"
    BASIC = "초급"
    INTERMEDIATE = "중급"
    ADVANCED = "고급"


class DetailLevel(str, Enum):
    """Summary detail levels"""
    SHORT = "short"
    NORMAL = "normal"
    DETAILED = "detailed"


class Chapter(BaseModel):
    """Chapter information"""
    timestamp_seconds: int
    timestamp_label: str  # e.g., "00:05:30"
    title: str
    summary: str


class ImportantTerm(BaseModel):
    """Important terminology"""
    term: str
    description: str


class Quiz(BaseModel):
    """Quiz item"""
    question: str
    answer: str


class SummaryResult(BaseModel):
    """Complete summary result"""
    title: str
    one_line_summary: str
    overview: str
    key_points: List[str]
    chapters: List[Chapter]
    important_terms: List[ImportantTerm]
    action_items: List[str]
    quiz: List[Quiz]
    target_audience: str
    difficulty: DifficultyLevel


class VideoInfoResponse(BaseModel):
    """Video information response"""
    video_id: str
    title: str
    channel: str
    thumbnail_url: str
    available_languages: List[str]
    original_url: str


class SummarizeRequest(BaseModel):
    """Summarize request"""
    url: str = Field(..., description="YouTube URL")
    transcript_language: str = Field("ko", description="Language to fetch transcripts")
    output_language: str = Field("ko", description="Language for the summary output")
    detail_level: DetailLevel = Field(DetailLevel.NORMAL, description="Summary detail level")


class SummarizeResponse(BaseModel):
    """Summarize response"""
    video_id: str
    title: str
    channel: str
    thumbnail_url: str
    summary: SummaryResult
    transcript_language: str
    output_language: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None
