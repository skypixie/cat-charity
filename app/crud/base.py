from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
        self,
        obj_in: BaseModel,
        session: AsyncSession,
        to_be_committed: bool,
        **kwargs,
    ):
        new_obj = self.model(**obj_in.model_dump(), **kwargs)

        session.add(new_obj)
        if to_be_committed:
            await session.commit()
            await session.refresh(new_obj)

        return new_obj

    async def update(
        self,
        db_obj,
        obj_in: BaseModel,
        session: AsyncSession,
        *,
        to_be_committed: bool,
    ):
        db_obj_data = jsonable_encoder(db_obj)
        obj_in_data = obj_in.model_dump(exclude_unset=True, exclude_none=True)

        for field in obj_in_data:
            if field in db_obj_data:
                setattr(db_obj, field, obj_in_data[field])

        session.add(db_obj)
        if to_be_committed:
            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
