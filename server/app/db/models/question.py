from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DATE, INTEGER, TEXT

from app.db import DeclarativeBase


class Question(DeclarativeBase):
    __tablename__ = "question"

    id = Column(
        INTEGER,
        autoincrement=True,
        primary_key=True,
        unique=True,
        doc="Unique index of element",
    )
    question_id = Column(
        INTEGER,
        nullable=False,
        index=True,
        unique=True,
        doc="Unique index of question",
    )
    question = Column(
        TEXT,
        nullable=False,
        unique=True,
        doc="Text of question",
    )
    answer = Column(
        TEXT,
        nullable=False,
        unique=True,
        doc="Text of answer",
    )
    created_at = Column(
        DATE,
        nullable=False,
        doc="Date the question was created",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
