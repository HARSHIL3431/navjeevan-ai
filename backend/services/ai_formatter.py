import json
import logging
from concurrent.futures import ThreadPoolExecutor
from backend.models.dtos import AdvisoryDTO
from backend.config.settings import settings

logger = logging.getLogger(__name__)

try:
    from groq import Groq
except ImportError:
    Groq = None

class AIFormatterService:
    def __init__(self):
        self.api_key = settings.groq_api_key.strip()
        self.model = settings.groq_model
        if self.api_key and Groq:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

    async def format_advisory(self, advisory: AdvisoryDTO) -> str:
        """Translates strict AdvisoryDTO into natural language."""
        if not self.client:
            logger.warning("Groq client unavailable. Returning raw fallback message.")
            return "Advisory generated (AI unavailable): " + str(advisory.crop_stage.stage)
            
        system_prompt = (
            "You are Navjeevan AI, an expert agricultural assistant. "
            "You receive strict JSON data representing crop stage, weather, pests, fertilizer, and irrigation logic. "
            "Your ONLY job is to explain this data naturally to a farmer in English. "
            "Do NOT invent new data. Do NOT add new recommendations. Only format what is provided."
        )
        
        # We must convert DTO to dict for JSON serialization
        import dataclasses
        dto_json = json.dumps(dataclasses.asdict(advisory), default=str)
        
        user_prompt = f"Format the following agricultural advisory data into a helpful response:\n\n{dto_json}"

        def _run():
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.3, # Low temp for deterministic formatting
            )
            return completion.choices[0].message.content

        try:
            with ThreadPoolExecutor() as executor:
                # Wrap synchronous groq call in thread
                response = executor.submit(_run).result(timeout=settings.groq_timeout_seconds)
            return response
        except TimeoutError:
            logger.warning("Groq AI formatting timed out")
            return "Your advisory is ready, but the AI explanation timed out. Please check the raw data."
        except Exception as e:
            logger.exception("Groq AI formatting failed")
            return "An error occurred while formatting your advisory."
