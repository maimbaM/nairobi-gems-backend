import os
from services.llm.engines.gemini import GeminiLLMService


def get_llm_service():
    """
    Returns an instance of the current selected LLM service.
    :return: LLM service instance
    """
    # Easily switch between different LLM engines by changing the env variable
    engine = os.environ.get("CURRENT_LLM_ENGINE", "gemini")
    if engine == "gemini":
        return GeminiLLMService()
