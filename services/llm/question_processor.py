from models.models import Question
from services.llm.engines.selector import get_llm_service


class QuestionProcessor:
    def __init__(self):
        self.llm_service = get_llm_service()

    async def process_question(self, question: Question) -> str:
        """
        Processes the question by generating a response using the LLM service.
        :param question: The question to be processed
        :return: The response from the LLM service
        """
        response = self.llm_service.generate_response(question.question)
        return response
