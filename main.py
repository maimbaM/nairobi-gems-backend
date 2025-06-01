import logging
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from models.models import Question
from config.logging_config import setup_logging
from services.llm.question_processor import QuestionProcessor

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)


@app.post(
    "/webhook",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Helps users discover hidden gems in Nairobi",
    description="Accepts questions and returns AI-generated recommendations.",
    responses={
        200: {
            "description": "Successful response with recommendations",
            "content": {
                "application/json": {
                    "example": {
                        "answer": {
                            "places": [
                                {
                                    "name": "Oloolua Nature Trail",
                                    "location": "Karen",
                                    "budget": "$",
                                    "description": "A lush, winding trail with caves and waterfalls",
                                    "best_time": "Weekday mornings",
                                    "good_for": "Solo walks, couples, small groups"
                                }
                            ]
                        }
                    }
                }
            }
        },
        400: {
            "description": "Missing question parameter",
            "content": {
                "application/json": {
                    "example": {"answer": "A question is required"}
                }
            }
        },
        500: {
            "description": "Server error",
            "content": {
                "application/json": {
                    "example": {"error": "Error processing question"}
                }
            }
        }
    }
)
async def handle_webhook(request: Request):
    """
    Handle incoming requests from the Nairobi Gems Frontend
    :param: request
    :return: response
    """
    try:
        body = await request.json()
        question = body.get("question")
        if not question:
            return JSONResponse(content={"answer": "A question is required"}, status_code=400)
        question = Question(question=question)
        question_processor = QuestionProcessor()
        answer = await question_processor.process_question(question=question)
        if not answer:
            return JSONResponse(content={"answer": "No answer generated"}, status_code=200)
        return JSONResponse(content={"answer": answer}, status_code=200)
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


handler = Mangum(app)


def lambda_handler(event, context):
    """
    AWS Lambda handler function
    :param event: The event data
    :param context: The context object
    :return: Response from the FastAPI app
    """
    logger.info(f"Received event: {event}")
    return handler(event, context)
