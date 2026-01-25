from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Donation(BaseModel):
    comment: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
