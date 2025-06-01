import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import AsyncMock, patch
from httpx import ASGITransport

from main import app


@pytest.fixture
def test_client():
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    )


@pytest.mark.asyncio
@patch("main.QuestionProcessor")
async def test_handle_webhook_success(mock_question_processor, test_client):
    mock_processor_instance = mock_question_processor.return_value
    mock_processor_instance.process_question = AsyncMock(
        return_value={"places": [{"name": "Test Place", "location": "Test Location"}]})

    response = await test_client.post("/webhook", json={"question": "Test question"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"answer": {"places": [{"name": "Test Place", "location": "Test Location"}]}}


@pytest.mark.asyncio
async def test_handle_webhook_missing_question(test_client):
    response = await test_client.post("/webhook", json={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"answer": "A question is required"}


@pytest.mark.asyncio
@patch("main.QuestionProcessor")
async def test_handle_webhook_empty_answer(mock_question_processor, test_client):
    mock_processor_instance = mock_question_processor.return_value
    mock_processor_instance.process_question = AsyncMock(return_value=None)

    response = await test_client.post("/webhook", json={"question": "Test question"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"answer": "No answer generated"}


@pytest.mark.asyncio
@patch("main.QuestionProcessor", side_effect=Exception("Something went wrong"))
async def test_handle_webhook_exception(mock_question_processor, test_client):
    response = await test_client.post("/webhook", json={"question": "Test question"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.json()
    assert response.json()["error"] == "Something went wrong"