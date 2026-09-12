"""Conftest for pytest"""

import pytest


@pytest.fixture
def sample_transcript():
    """Sample transcript data for testing"""
    return [
        {"text": "Welcome to the lecture.", "start": 0, "duration": 2},
        {"text": "Today we'll discuss important topics.", "start": 2, "duration": 3},
        {"text": "First, let's cover the basics.", "start": 5, "duration": 2},
        {"text": "This is fundamental knowledge.", "start": 7, "duration": 3},
    ]
