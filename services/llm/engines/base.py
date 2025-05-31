from abc import ABC, abstractmethod


class BaseLLMService(ABC):

    @abstractmethod
    def generate_response(self, question: str) -> str:
        pass
