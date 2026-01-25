from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation
from app.models.charity_project import CharityProject


async def get_not_full_donations(
    session: AsyncSession
) -> list[Donation]:
    donations_with_money = await session.execute(
        select(Donation).where(
            ~Donation.fully_invested
        )
    )
    return donations_with_money.scalars().all()


async def get_not_full_projects(
    session: AsyncSession
) -> list[CharityProject]:
    projects_not_full = await session.execute(
        select(CharityProject).where(
            ~CharityProject.fully_invested
        )
    )
    return projects_not_full.scalars().all()


async def invest_left_money(
    session: AsyncSession,
    project_to_add_to_session: Optional[CharityProject] = None,
    donation_to_add_to_session: Optional[Donation] = None
):
    """
    Инвестирует средства из пожертвований, где остались деньги.

    Проставляет значения в проектах и пожертвованиях.
    """
    donations_with_money = await get_not_full_donations(session)
    if donation_to_add_to_session is not None:
        donations_with_money.append(donation_to_add_to_session)

    projects_not_full = await get_not_full_projects(session)
    if project_to_add_to_session is not None:
        projects_not_full.append(project_to_add_to_session)

    for project in projects_not_full:
        left_to_invest = project.full_amount - project.invested_amount

        for donation in donations_with_money:
            left_money = donation.full_amount - donation.invested_amount

            if left_to_invest > left_money:
                # инвестировать оставшиеся деньги в проект
                donation.invested_amount += left_money
                project.invested_amount += left_money

                left_to_invest -= left_money
            else:
                # инвестировать разницу
                donation.invested_amount += left_to_invest
                project.invested_amount += left_to_invest

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
            session.add(donation)

        if project.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        session.add(project)