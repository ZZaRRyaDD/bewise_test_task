from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Question


class QuestionRepository:
    async def get_last(self, session: AsyncSession) -> Question | None:
        query = select(Question).order_by(Question.id.desc()).limit(1)
        result = await session.execute(query)
        return result.scalar()

    async def get_by_question_id(self, session: AsyncSession, ids: list) -> list[Question]:
        query = select(Question).where(Question.question_id.in_(ids))
        result = await session.execute(query)
        return result.scalars().all()

    async def check_exists_by_question_id(self, session: AsyncSession, question_id: int) -> bool:
        query = select(exists().where(Question.question_id == question_id))
        exist = await session.scalar(query)
        return exist

    async def bulk_create(self, session: AsyncSession, objs: list[dict]) -> None:
        await session.execute(
            insert(Question),
            objs,
        )
        await session.commit()
