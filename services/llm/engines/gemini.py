import os
import re
import json

from services.llm.engines.base import BaseLLMService
from google import genai
from services.llm.prompts.prompt import get_llm_prompt


class GeminiLLMService(BaseLLMService):
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-preview-04-17")

    def generate_response(self, question: str) -> str:
        try:
            prompt = get_llm_prompt(question=question)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            if not response or not response.text:
                return "No response generated from Gemini LLM."
            match = re.search(r'{.*}', response.text.strip(), re.DOTALL)
            if match:
                try:
                    cleaned_json = json.loads(match.group())
                    return cleaned_json
                except json.JSONDecodeError as e:
                    raise ValueError(f"JSON decoding failed:{e}")
        except Exception as e:
            raise Exception(f"Error generating response: {e}")
