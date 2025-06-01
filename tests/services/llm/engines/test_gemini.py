import json
import pytest
from unittest.mock import MagicMock, patch
from services.llm.engines.gemini import GeminiLLMService


@patch("services.llm.engines.gemini.genai.Client")
def test_generate_response(mock_client_class):
    mock_response = MagicMock()
    mock_response.text = json.dumps([{"name": "Test Place", "location": "Test Location"}])

    mock_model = MagicMock()
    mock_model.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_model

    service = GeminiLLMService()
    question = "What are some good places to visit?"
    result = service.generate_response(question=question)

    assert "places" in result
    assert isinstance(result["places"], list)
    assert result["places"][0]["name"] == "Test Place"

