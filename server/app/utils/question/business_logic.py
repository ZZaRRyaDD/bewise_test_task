from typing import Sequence

import aiohttp
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Question
from app.db.repository import QuestionRepository
from app.schemas.question import RequestQuestionSchema


async def send_request(
    params: dict,
    url: str = "https://jservice.io/api/random",
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            return await response.json()


async def get_parsed_questions(count: int) -> list[RequestQuestionSchema]:
    params = {"count": count}
    questions = await send_request(params)
    return parse_obj_as(list[RequestQuestionSchema], questions)


async def create_or_request_questions(
    count: int,
    session: AsyncSession,
) -> Question | None:
    question_repository = QuestionRepository()
    last_item = await question_repository.get_last(session)

    parsed_questions = await get_parsed_questions(count)

    questions_ids = set(question.question_id for question in parsed_questions)

    exists_items = await question_repository.get_by_question_id(
        session,
        questions_ids,
    )
    processed = set(item.question_id for item in exists_items)

    questions_to_create = []
    for question in parsed_questions:
        if question.question_id not in processed:
            questions_to_create.append(question.dict())
            processed.add(question.question_id)
        else:
            is_exists = True
            while is_exists and question.question_id in processed:
                question = (await get_parsed_questions(1))[0]
                is_exists = await question_repository.check_exists_by_question_id(
                    session,
                    question_id=question.question_id,
                )
            processed.add(question.question_id)
            questions_to_create.append(question.dict())

    await question_repository.bulk_create(session, questions_to_create)

    return last_item
