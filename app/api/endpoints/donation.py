from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB
)
from app.services.investments import invest_left_money


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True
)
async def get_all_donations(session: SessionDep):
    """Показать список всех пожертвований."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    obj_in: DonationCreate,
    session: SessionDep
):
    """Создать пожертвование."""
    donation_db = await donation_crud.create(
        obj_in,
        session,
        to_be_committed=False,
        invested_amount=0
    )
    await invest_left_money(session, donation_to_add_to_session=donation_db)

    session.add(donation_db)
    await session.commit()
    await session.refresh(donation_db)

    return donation_db
