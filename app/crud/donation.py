from typing import List

from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        None
    ]
):

    async def get_donations_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def get_not_fully_invested_objects(
        self,
        session: AsyncSession
    ):
        return (
            await session.execute(
                select(self.model).where(not_(self.model.fully_invested))
            )
        ).scalars().all()


donation_crud = CRUDDonation(Donation)
