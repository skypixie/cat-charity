from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class BaseModel(CommonMixin, Base):
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now
    )
    close_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )
