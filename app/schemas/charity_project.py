from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.constants import (
    MIN_PROJ_DESC_LENGTH,
    MIN_PROJ_NAME_LENGTH,
    MAX_PROJ_NAME_LENGTH
)


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_PROJ_NAME_LENGTH,
        max_length=MAX_PROJ_NAME_LENGTH
    )
    description: str = Field(
        ...,
        min_length=MIN_PROJ_DESC_LENGTH
    )
    full_amount: int = Field(..., ge=1)

    model_config = ConfigDict(
        extra='forbid'
    )


class CharityProjectCreate(CharityProjectBase):
    ...


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(
        None,
        min_length=MIN_PROJ_NAME_LENGTH,
        max_length=MAX_PROJ_NAME_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_PROJ_DESC_LENGTH
    )
    full_amount: Optional[int] = Field(None, ge=1)


class CharityProjectDB(CharityProjectCreate):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )
