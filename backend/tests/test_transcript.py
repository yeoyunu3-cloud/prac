"""Tests for transcript processing"""

import pytest
from app.services.transcript import (
    TranscriptSegment,
    TranscriptChunk,
    split_transcript_into_chunks
)


class TestTranscriptSegment:
    """Test TranscriptSegment class"""
    
    def test_create_segment(self):
        """Test creating a segment"""
        segment = TranscriptSegment("Hello world", 0.0, 2.5)
        assert segment.text == "Hello world"
        assert segment.start == 0.0
        assert segment.duration == 2.5
        assert segment.end == 2.5
    
    def test_segment_to_dict(self):
        """Test converting segment to dictionary"""
        segment = TranscriptSegment("Test text", 5.0, 3.0)
        data = segment.to_dict()
        assert data["text"] == "Test text"
        assert data["start"] == 5.0
        assert data["duration"] == 3.0


class TestTranscriptChunk:
    """Test TranscriptChunk class"""
    
    def test_create_chunk(self):
        """Test creating a chunk"""
        segments = [
            TranscriptSegment("Part 1", 0.0, 2.0),
            TranscriptSegment("Part 2", 2.0, 3.0)
        ]
        chunk = TranscriptChunk(segments, 0)
        
        assert chunk.chunk_index == 0
        assert len(chunk.segments) == 2
        assert chunk.start_time == 0.0
        assert chunk.end_time == 5.0
        assert "Part 1" in chunk.full_text
        assert "Part 2" in chunk.full_text


class TestSplitTranscriptIntoChunks:
    """Test transcript chunking"""
    
    def test_split_small_transcript(self):
        """Test chunking a small transcript"""
        segments = [
            {"text": "Hello", "start": 0, "duration": 1},
            {"text": "world", "start": 1, "duration": 1}
        ]
        chunks = split_transcript_into_chunks(segments, max_chunk_length=100)
        assert len(chunks) == 1
        assert chunks[0].full_text == "Hello world"
    
    def test_split_large_transcript(self):
        """Test chunking a large transcript"""
        segments = [
            {"text": "word" * 100, "start": i, "duration": 1}
            for i in range(10)
        ]
        chunks = split_transcript_into_chunks(segments, max_chunk_length=500)
        assert len(chunks) > 1
    
    def test_chunk_boundary_integrity(self):
        """Test that chunk boundaries respect segment boundaries"""
        segments = [
            {"text": "Sentence one.", "start": 0, "duration": 2},
            {"text": "Sentence two.", "start": 2, "duration": 2},
            {"text": "Sentence three.", "start": 4, "duration": 2}
        ]
        chunks = split_transcript_into_chunks(segments, max_chunk_length=50)
        
        # Verify all segments are accounted for
        all_text = " ".join(chunk.full_text for chunk in chunks)
        assert "Sentence one" in all_text
        assert "Sentence two" in all_text
        assert "Sentence three" in all_text
    
    def test_empty_transcript(self):
        """Test chunking empty transcript"""
        chunks = split_transcript_into_chunks([])
        assert len(chunks) == 0
