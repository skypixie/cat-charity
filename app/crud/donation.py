from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class DonationCRUD(CRUDBase):
    async def get_donation_for_user(
        self,
        session: AsyncSession,
        user_id: int
    ):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)
