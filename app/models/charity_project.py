from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.constants import (
    MIN_PROJ_NAME_LENGTH,
    MAX_PROJ_NAME_LENGTH,
    MIN_PROJ_DESC_LENGTH
)
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name: Mapped[str] = mapped_column(
        String(MAX_PROJ_NAME_LENGTH),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    @validates('name')
    def validate_name_length(self, key, name):
        name = name.strip()
        if not (
            MIN_PROJ_NAME_LENGTH <= len(name) <= MAX_PROJ_NAME_LENGTH
        ):
            raise ValueError(
                'Название проекта должно быть'
                f' длиной от {MIN_PROJ_NAME_LENGTH} '
                f'до {MAX_PROJ_NAME_LENGTH} символов.'
            )
        return name

    @validates('description')
    def validate_description_min_length(self, key, description):
        description = description.strip()
        if len(description) < MIN_PROJ_DESC_LENGTH:
            raise ValueError(
                'Описание проекта должно '
                f'быть длиннее {MIN_PROJ_DESC_LENGTH} символов.'
            )
        return description
