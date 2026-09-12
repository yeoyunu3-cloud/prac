"""Tests for YouTube utilities"""

import pytest
from app.utils.youtube import extract_video_id, is_valid_youtube_url, validate_video_id


class TestExtractVideoId:
    """Test video ID extraction from various URL formats"""
    
    def test_extract_from_standard_url(self):
        """Test extraction from standard youtube.com URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_from_youtu_be(self):
        """Test extraction from shortened youtu.be URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_from_shorts_url(self):
        """Test extraction from YouTube Shorts URL"""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_with_timestamp_parameter(self):
        """Test extraction from URL with timestamp"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=123s"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_with_list_parameter(self):
        """Test extraction from URL with playlist parameter"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLxxx"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_extract_from_youtu_be_with_params(self):
        """Test extraction from youtu.be with parameters"""
        url = "https://youtu.be/dQw4w9WgXcQ?t=10"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_invalid_url_returns_none(self):
        """Test that invalid URLs return None"""
        assert extract_video_id("https://google.com") is None
        assert extract_video_id("not a url") is None
    
    def test_empty_url_returns_none(self):
        """Test that empty URL returns None"""
        assert extract_video_id("") is None
        assert extract_video_id(None) is None


class TestIsValidYoutubeUrl:
    """Test YouTube URL validation"""
    
    def test_valid_standard_url(self):
        """Test valid standard YouTube URL"""
        assert is_valid_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") is True
    
    def test_valid_youtu_be_url(self):
        """Test valid youtu.be URL"""
        assert is_valid_youtube_url("https://youtu.be/dQw4w9WgXcQ") is True
    
    def test_valid_shorts_url(self):
        """Test valid YouTube Shorts URL"""
        assert is_valid_youtube_url("https://www.youtube.com/shorts/dQw4w9WgXcQ") is True
    
    def test_invalid_domain(self):
        """Test non-YouTube domain"""
        assert is_valid_youtube_url("https://google.com") is False
    
    def test_invalid_format(self):
        """Test invalid video ID format"""
        assert is_valid_youtube_url("https://www.youtube.com/watch?v=short") is False
    
    def test_non_url(self):
        """Test non-URL strings"""
        assert is_valid_youtube_url("not a url") is False
    
    def test_empty_string(self):
        """Test empty string"""
        assert is_valid_youtube_url("") is False


class TestValidateVideoId:
    """Test video ID format validation"""
    
    def test_valid_video_id(self):
        """Test valid video ID"""
        assert validate_video_id("dQw4w9WgXcQ") is True
    
    def test_video_id_with_underscore(self):
        """Test video ID with underscore"""
        assert validate_video_id("dQw4_9WgXcQ") is True
    
    def test_video_id_with_dash(self):
        """Test video ID with dash"""
        assert validate_video_id("dQw4-9WgXcQ") is True
    
    def test_too_short_video_id(self):
        """Test video ID that's too short"""
        assert validate_video_id("short") is False
    
    def test_too_long_video_id(self):
        """Test video ID that's too long"""
        assert validate_video_id("dQw4w9WgXcQdQw4w9WgXcQ") is False
    
    def test_video_id_with_special_chars(self):
        """Test video ID with invalid special characters"""
        assert validate_video_id("dQw4@9WgXcQ") is False
    
    def test_empty_video_id(self):
        """Test empty video ID"""
        assert validate_video_id("") is False
