from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from models.question import Question
from services.llm.question_processor import QuestionProcessor

app = FastAPI()
load_dotenv()


@app.post("/webhook")
async def handle_webhook(request: Request):
    """"
    Handle incoming requests from the Nairobi Gems Frontend
    :param: request
    :return: response
    """
    try:
        body = await request.json()
        question = body.get("question")
        if not question:
            return Response(content="Question is required", status_code=400)
        question = Question(question=question)
        question_processor = QuestionProcessor()
        answer = await question_processor.process_question(question=question)
        return Response(content=answer, media_type="text/plain", status_code=200)
    except Exception as e:
        return Response(content=f"An error occurred: {str(e)}", status_code=500)
