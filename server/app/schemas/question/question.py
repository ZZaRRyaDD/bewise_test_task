from datetime import date, datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator


class RequestCountQuestions(BaseModel):
    count: int = Field(default=1, alias="questions_num")

    @validator("count")
    def validate_count(cls, count):
        if count <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Count question must be more one")
        return count


class RequestQuestionSchema(BaseModel):
    question_id: int = Field(..., alias="id")
    question: str
    answer: str
    created_at: datetime


class QuestionSchema(BaseModel):
    question_id: int
    question: str
    answer: str
    created_at: date

    class Config:
        orm_mode = True


class ResponseQuestion(BaseModel):
    last_question: QuestionSchema | None = Field(None)
