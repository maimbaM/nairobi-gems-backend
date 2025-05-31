from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.question import Question
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


@app.post("/webhook")
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
        return JSONResponse(content={"answer": answer}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
