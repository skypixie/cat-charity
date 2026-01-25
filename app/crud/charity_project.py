from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):
    async def get_project_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == name
            )
        )
        return project.scalar()


charity_project_crud = CharityProjectCRUD(CharityProject)
