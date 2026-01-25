from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., ge=1)
    comment: Optional[str] = None

    model_config = ConfigDict(
        extra='forbid'
    )


class DonationCreate(DonationBase):
    ...

    model_config = ConfigDict(
        from_attributes=True
    )


class DonationDB(DonationBase):
    id: int
    create_date: datetime


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int
