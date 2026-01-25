from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.api.validators import (
    check_charity_project_name_duplicate,
    check_charity_project_exists,
    check_charity_project_not_closed,
    check_new_amount_more_than_invested,
    check_project_already_has_investments
)
from app.services.investments import invest_left_money


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(session: SessionDep):
    """Показать список всех целевых проектов."""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def create_charity_project(
    obj_in: CharityProjectCreate,
    session: SessionDep
):
    """Создать целевой проект."""
    await check_charity_project_name_duplicate(obj_in.name, session)
    new_project = await charity_project_crud.create(
        obj_in,
        session,
        to_be_committed=False,
        invested_amount=0
    )
    await invest_left_money(session, project_to_add_to_session=new_project)

    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep
):
    """
    Редактировать целевой проект.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    db_project = await check_charity_project_exists(project_id, session)
    check_charity_project_not_closed(db_project)
    if obj_in.name:
        await check_charity_project_name_duplicate(obj_in.name, session)

    if obj_in.full_amount:
        check_new_amount_more_than_invested(db_project, obj_in.full_amount)

    db_project = await charity_project_crud.update(
        db_project,
        obj_in,
        session,
        to_be_committed=False
    )
    await invest_left_money(session)
    await session.commit()
    await session.refresh(db_project)

    return db_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep
):
    """
    Удалить целевой проект.

    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    db_project = await check_charity_project_exists(project_id, session)
    check_project_already_has_investments(db_project)

    await charity_project_crud.remove(db_project, session)
    return db_project
