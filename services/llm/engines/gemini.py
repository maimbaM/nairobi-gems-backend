import os
import json
import logging
from google import genai
from services.llm.engines.base import BaseLLMService
from models.models import Place
from services.llm.prompts.prompt import get_llm_prompt

logger = logging.getLogger(__name__)


class GeminiLLMService(BaseLLMService):
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-preview-04-17")

    def generate_response(self, question: str) -> dict[str, str]:
        try:
            prompt = get_llm_prompt(question=question)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[Place],
                },
            )
            if not response or not response.text:
                logger.error("Received empty response from Gemini model.")
                raise Exception("Empty response from Gemini model.")
            return {"places": json.loads(response.text.strip())}
        except Exception as e:
            logger.error(f"Error generating response from Gemini: {e}")
            raise Exception(f"Error generating response: {e}")
