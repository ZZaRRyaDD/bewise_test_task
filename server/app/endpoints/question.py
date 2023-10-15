from fastapi import APIRouter, Body, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_session
from app.schemas.question import RequestCountQuestions, ResponseQuestion
from app.utils.question import create_or_request_questions


api_router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseQuestion,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Count must be more one",
        },
        status.HTTP_201_CREATED: {
            "description": "Success created",
        },
    },
)
async def get_and_create_questions(
    _: Request,
    body: RequestCountQuestions = Body(...),
    session: AsyncSession = Depends(get_session),
):
    question = await create_or_request_questions(body.count, session)
    return ResponseQuestion(last_question=question)
