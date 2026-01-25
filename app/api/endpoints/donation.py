from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB
)
from app.services.investments import invest_left_money


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UserDep = Annotated[User, Depends(current_user)]
SuperuserDep = Annotated[User, Depends(current_superuser)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(session: SessionDep):
    """Показать список всех пожертвований."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donation(
    obj_in: DonationCreate,
    session: SessionDep,
    user: UserDep
):
    """Создать пожертвование."""
    donation_db = await donation_crud.create(
        obj_in,
        session,
        to_be_committed=False,
        invested_amount=0,
        user_id=user.id
    )
    await invest_left_money(session, donation_to_add_to_session=donation_db)

    session.add(donation_db)
    await session.commit()
    await session.refresh(donation_db)

    return donation_db


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_user_donation(
    session: SessionDep,
    user: UserDep
):
    donations = await donation_crud.get_donation_for_user(
        session,
        user.id
    )
    return donations
