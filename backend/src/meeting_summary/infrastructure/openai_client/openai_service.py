"""OpenAI service for speech-to-text and text summarization"""

import json
from typing import Dict

import openai
from loguru import logger

from meeting_summary.config import openai_config
from .prompts import MEETING_SUMMARY_PROMPT
from meeting_summary.domain.exceptions.audio_exceptions import (
    SummarizationError,
    TranscriptionError
)


class OpenAIService:
    """Service for interacting with OpenAI APIs"""
    
    def __init__(self):
        self.config = openai_config
        self.client = openai.OpenAI(api_key=self.config.api_key.get_secret_value())
    
    async def transcribe_audio(self, file_path: str) -> Dict:
        """Transcribe audio file using OpenAI Whisper"""
        try:
            logger.info(f"Starting transcription for file: {file_path}")
            
            with open(file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model=self.config.model,
                    file=audio_file,
                    language=self.config.language,
                    response_format="verbose_json"
                )
            
            result = {
                "text": response.text,
                "language": response.language if hasattr(response, 'language') else self.config.language,
                "duration": response.duration if hasattr(response, 'duration') else None
            }
            
            logger.info(f"Transcription completed successfully. Text length: {len(result['text'])}")
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise TranscriptionError(f"Failed to transcribe audio: {e}")
    
    async def summarize_meeting(self, transcription: str) -> Dict:
        """Summarize transcription into structured meeting notes"""
        try:
            logger.info(f"Starting meeting summarization. Text length: {len(transcription)}")
            
            user_prompt = MEETING_SUMMARY_PROMPT.format(transcription=transcription)
            
            response = self.client.chat.completions.create(
                model=self.config.chat_model,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=2000
            )
            
            # Parse JSON response
            content = response.choices[0].message.content.strip()
            logger.debug(f"Raw OpenAI response: {content}")
            
            try:
                # Try to extract JSON from response if it's wrapped in markdown or other text
                import re
                
                # Look for JSON block in markdown format
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    # Look for any JSON object
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                    else:
                        # If no JSON found, try parsing the whole content
                        json_str = content
                
                result = json.loads(json_str)
                logger.info("Meeting summarization completed successfully")
                logger.debug(f"Parsed result: {result}")
                
                # Ensure all required fields exist with proper types
                return {
                    "summary": str(result.get("summary", "")),
                    "key_points": list(result.get("key_points", [])),
                    "action_items": list(result.get("action_items", [])), 
                    "participants": list(result.get("participants", [])),
                    "meeting_duration": result.get("meeting_duration", None)
                }
                
            except (json.JSONDecodeError, AttributeError) as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                logger.debug(f"Raw content: {content}")
                
                # Fallback: create a simple structure from the response
                return {
                    "summary": content,
                    "key_points": [],
                    "action_items": [],
                    "participants": [],
                    "meeting_duration": None
                }
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise SummarizationError(f"Failed to summarize meeting: {e}")
