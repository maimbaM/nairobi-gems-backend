import os
import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_environment():
    os.environ["GEMINI_API_KEY"] = "test_gemini_api_key"
    os.environ["GEMINI_MODEL"] = "test_gemini_model"
