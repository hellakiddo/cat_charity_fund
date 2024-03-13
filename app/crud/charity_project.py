from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):

    async def get_charity_project_id_by_name(
            self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        return (
            await session.execute(
                select(CharityProject.id).where(
                    CharityProject.name == project_name
                ))).scalars().first()

    async def get_charity_project_close_date(
            self, project_id: int, session: AsyncSession):
        return (
            await session.execute(
                select(
                    CharityProject.close_date
                ).where(CharityProject.id == project_id))).scalars().first()

    async def get_charity_project_invested_amount(
            self, project_id: int, session: AsyncSession):
        return (
            await session.execute(select(
                CharityProject.invested_amount
            ).where(CharityProject.id == project_id))).scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
