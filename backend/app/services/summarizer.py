"""Claude API integration for summarization"""

import json
import asyncio
from typing import Optional, List
from anthropic import Anthropic, APIError
from app.schemas.models import SummaryResult, DetailLevel
from app.services.transcript import TranscriptChunk


def get_summary_prompt(
    transcript_text: str,
    detail_level: DetailLevel = DetailLevel.NORMAL,
    output_language: str = "ko"
) -> str:
    """
    Generate prompt for Claude to summarize transcript.
    
    Args:
        transcript_text: The transcript text to summarize
        detail_level: Level of detail (short, normal, detailed)
        output_language: Output language code
        
    Returns:
        Prompt string
    """
    
    language_name = "Korean" if output_language == "ko" else "English"
    
    detail_instructions = {
        DetailLevel.SHORT: "Very concise (2-3 sentences per section)",
        DetailLevel.NORMAL: "Balanced and comprehensive",
        DetailLevel.DETAILED: "Comprehensive with examples and context"
    }
    
    detail_desc = detail_instructions.get(detail_level, detail_instructions[DetailLevel.NORMAL])
    
    prompt = f"""Please analyze the following transcript from a YouTube lecture and provide a structured summary in JSON format (respond ONLY with valid JSON, no additional text).

Output language: {language_name}
Detail level: {detail_desc}
Transcript:
---
{transcript_text}
---

Provide the response EXACTLY in this JSON format (all fields required, use [{language_name}] language):

{{
  "title": "Lecture title based on the transcript",
  "one_line_summary": "One sentence summary",
  "overview": "2-3 paragraph overview of the entire lecture",
  "key_points": ["point 1", "point 2", "point 3", ...],
  "chapters": [
    {{
      "timestamp_minutes": XX,
      "title": "Chapter title",
      "summary": "Brief summary of this section"
    }}
  ],
  "important_terms": [
    {{
      "term": "Technical term",
      "description": "Explanation of the term"
    }}
  ],
  "action_items": ["What to do with this knowledge", ...],
  "quiz": [
    {{
      "question": "Test question",
      "answer": "Correct answer"
    }},
    {{
      "question": "Another question",
      "answer": "Correct answer"
    }}
  ],
  "target_audience": "Who should watch this lecture",
  "difficulty": "입문|초급|중급|고급"
}}

IMPORTANT RULES:
1. Use ONLY information from the transcript - do NOT add external knowledge
2. If information is unclear, mark it as uncertain
3. Ensure all JSON is valid and properly formatted
4. Do NOT include any text outside the JSON
5. All fields must be present in the response
6. For chapters, use timestamps from the transcript (in minutes from start)
7. Keep summaries factual and based on transcript content"""

    return prompt


async def summarize_chunk(
    client: Anthropic,
    chunk_text: str,
    output_language: str = "ko",
    model: str = "claude-3-5-sonnet-20241022"
) -> str:
    """
    Summarize a single transcript chunk.
    
    Args:
        client: Anthropic client
        chunk_text: Transcript text to summarize
        output_language: Output language
        model: Model name
        
    Returns:
        Summary text
    """
    
    prompt = f"""Summarize the following transcript segment in {output_language}.
Keep it concise and factual - only use information from the transcript.

Transcript:
{chunk_text}

Provide a 2-3 paragraph summary:"""
    
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text


async def summarize_transcript(
    transcript_text: str,
    detail_level: DetailLevel = DetailLevel.NORMAL,
    output_language: str = "ko",
    model: str = "claude-3-5-sonnet-20241022",
    api_key: str = None
) -> SummaryResult:
    """
    Summarize a full transcript using Claude API.
    
    Args:
        transcript_text: Full transcript text
        detail_level: Summary detail level
        output_language: Output language
        model: Claude model name
        api_key: Anthropic API key
        
    Returns:
        SummaryResult object
        
    Raises:
        APIError: If API call fails after retries
    """
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not provided")
    
    client = Anthropic(api_key=api_key)
    prompt = get_summary_prompt(transcript_text, detail_level, output_language)
    
    # Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response.content[0].text
            
            # Try to parse JSON
            try:
                summary_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to repair JSON by extracting it
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        summary_data = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        if attempt < max_retries - 1:
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        raise ValueError("Failed to parse Claude response as JSON")
                else:
                    raise ValueError("No JSON found in Claude response")
            
            # Convert to SummaryResult 
            return _convert_to_summary_result(summary_data)
            
        except APIError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise


def _convert_to_summary_result(data: dict) -> SummaryResult:
    """Convert raw data from Claude to SummaryResult object"""
    
    from app.schemas.models import Chapter, ImportantTerm, Quiz, DifficultyLevel
    
    # Parse difficulty level
    difficulty_str = data.get("difficulty", "초급").strip()
    try:
        difficulty = DifficultyLevel(difficulty_str)
    except ValueError:
        difficulty = DifficultyLevel.BASIC
    
    # Parse chapters
    chapters = []
    for ch_data in data.get("chapters", []):
        try:
            # Convert minutes to seconds if needed
            timestamp = ch_data.get("timestamp_minutes", 0)
            if isinstance(timestamp, str):
                # Parse "MM:SS" format
                parts = timestamp.split(":")
                if len(parts) == 2:
                    timestamp = int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:
                    timestamp = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                timestamp = int(timestamp) * 60  # minutes to seconds
            
            # Generate timestamp label
            hours = timestamp // 3600
            minutes = (timestamp % 3600) // 60
            seconds = timestamp % 60
            if hours > 0:
                timestamp_label = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                timestamp_label = f"{minutes:02d}:{seconds:02d}"
            
            chapter = Chapter(
                timestamp_seconds=timestamp,
                timestamp_label=timestamp_label,
                title=ch_data.get("title", ""),
                summary=ch_data.get("summary", "")
            )
            chapters.append(chapter)
        except Exception:
            pass  # Skip malformed chapters
    
    # Parse important terms
    terms = []
    for term_data in data.get("important_terms", []):
        try:
            term = ImportantTerm(
                term=term_data.get("term", ""),
                description=term_data.get("description", "")
            )
            terms.append(term)
        except Exception:
            pass
    
    # Parse quiz
    quiz = []
    for quiz_data in data.get("quiz", []):
        try:
            q = Quiz(
                question=quiz_data.get("question", ""),
                answer=quiz_data.get("answer", "")
            )
            quiz.append(q)
        except Exception:
            pass
    
    return SummaryResult(
        title=data.get("title", ""),
        one_line_summary=data.get("one_line_summary", ""),
        overview=data.get("overview", ""),
        key_points=data.get("key_points", []),
        chapters=chapters,
        important_terms=terms,
        action_items=data.get("action_items", []),
        quiz=quiz,
        target_audience=data.get("target_audience", ""),
        difficulty=difficulty
    )


async def summarize_long_transcript(
    chunks: List[TranscriptChunk],
    detail_level: DetailLevel = DetailLevel.NORMAL,
    output_language: str = "ko",
    model: str = "claude-3-5-sonnet-20241022",
    api_key: str = None
) -> str:
    """
    Summarize a long transcript using map-reduce approach.
    
    1. Summarize each chunk individually
    2. Combine chunk summaries
    3. Generate final summary
    
    Args:
        chunks: List of TranscriptChunk objects
        detail_level: Summary detail level
        output_language: Output language
        model: Claude model name
        api_key: Anthropic API key
        
    Returns:
        Combined summary text
    """
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not provided")
    
    client = Anthropic(api_key=api_key)
    
    # Step 1: Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        try:
            summary = await summarize_chunk(
                client, 
                chunk.full_text, 
                output_language,
                model
            )
            chunk_summaries.append(summary)
        except Exception as e:
            # Log error but continue
            chunk_summaries.append(f"[Error summarizing chunk {chunk.chunk_index}]")
    
    # Step 2: Combine chunk summaries
    combined_text = "\n\n".join([
        f"Section {i+1}:\n{summary}"
        for i, summary in enumerate(chunk_summaries)
    ])
    
    # Step 3: Generate final summary from combined text
    final_prompt = f"""Based on these summaries of different sections, create a comprehensive summary in {output_language}:

{combined_text}

Provide a unified 3-4 paragraph summary that integrates all sections:"""
    
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )
    
    return response.content[0].text
