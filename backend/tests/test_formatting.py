"""Tests for formatting utilities"""

from app.utils.formatting import seconds_to_timestamp, timestamp_to_seconds, build_youtube_timestamp_url


class TestSecondsToTimestamp:
    """Test seconds to timestamp conversion"""
    
    def test_less_than_minute(self):
        """Test seconds less than 60"""
        assert seconds_to_timestamp(30) == "00:30"
    
    def test_exactly_minute(self):
        """Test exactly 60 seconds"""
        assert seconds_to_timestamp(60) == "01:00"
    
    def test_minutes_and_seconds(self):
        """Test minutes and seconds"""
        assert seconds_to_timestamp(125) == "02:05"
    
    def test_with_hours(self):
        """Test with hours"""
        assert seconds_to_timestamp(3661) == "01:01:01"
    
    def test_zero_seconds(self):
        """Test zero seconds"""
        assert seconds_to_timestamp(0) == "00:00"
    
    def test_negative_seconds(self):
        """Test negative seconds returns 00:00"""
        assert seconds_to_timestamp(-10) == "00:00"


class TestTimestampToSeconds:
    """Test timestamp to seconds conversion"""
    
    def test_mm_ss_format(self):
        """Test MM:SS format"""
        assert timestamp_to_seconds("02:05") == 125
    
    def test_hh_mm_ss_format(self):
        """Test HH:MM:SS format"""
        assert timestamp_to_seconds("01:01:01") == 3661
    
    def test_single_digit_seconds(self):
        """Test single digit seconds"""
        assert timestamp_to_seconds("01:05") == 65
    
    def test_zero_timestamp(self):
        """Test zero timestamp"""
        assert timestamp_to_seconds("00:00") == 0


class TestBuildYoutubeTimestampUrl:
    """Test YouTube timestamp URL building"""
    
    def test_build_url_with_seconds(self):
        """Test building URL with timestamp"""
        url = build_youtube_timestamp_url("dQw4w9WgXcQ", 123)
        assert url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=123s"
    
    def test_build_url_with_zero_seconds(self):
        """Test building URL with zero timestamp"""
        url = build_youtube_timestamp_url("dQw4w9WgXcQ", 0)
        assert url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=0s"
