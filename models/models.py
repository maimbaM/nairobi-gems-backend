from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Place(BaseModel):
    name: str
    location: str
    budget: str
    description: str
    best_time: str
    good_for: str
