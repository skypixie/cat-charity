from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject

from app.constants import (
    ERR_MSG_CANT_DELETE_PROJECT,
    ERR_MSG_CANT_FIND_PROJECT,
    ERR_MSG_CANT_LOWER_AMOUNT,
    ERR_MSG_CLOSED_PROJECT,
    ERR_MSG_DUPLICATE_PROJECT,
    ERR_CODE_CANT_DELETE_PROJECT,
    ERR_CODE_CANT_FIND_PROJECT,
    ERR_CODE_CANT_LOWER_AMOUNT,
    ERR_CODE_CLOSED_PROJECT,
    ERR_CODE_DUPLICATE_PROJECT
)
from app.crud.charity_project import charity_project_crud


async def check_charity_project_name_duplicate(
    name: str,
    session: AsyncSession
) -> None:
    project = await charity_project_crud.get_project_by_name(name, session)

    if project is not None:
        raise HTTPException(
            status_code=ERR_CODE_DUPLICATE_PROJECT,
            detail=ERR_MSG_DUPLICATE_PROJECT
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=ERR_CODE_CANT_FIND_PROJECT,
            detail=ERR_MSG_CANT_FIND_PROJECT
        )
    return project


def check_charity_project_not_closed(
    db_project: CharityProject
) -> None:
    if db_project.fully_invested:
        raise HTTPException(
            status_code=ERR_CODE_CLOSED_PROJECT,
            detail=ERR_MSG_CLOSED_PROJECT
        )


def check_new_amount_more_than_invested(
    db_project: CharityProject,
    new_full_amount: int
):
    if db_project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=ERR_CODE_CANT_LOWER_AMOUNT,
            detail=ERR_MSG_CANT_LOWER_AMOUNT
        )


def check_project_already_has_investments(
    db_project: CharityProject
):
    if db_project.invested_amount > 0:
        raise HTTPException(
            status_code=ERR_CODE_CANT_DELETE_PROJECT,
            detail=ERR_MSG_CANT_DELETE_PROJECT
        )
