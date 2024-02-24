from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models.charity_project import CharityProject
from app.models.donation import Donation

async def get_not_invested_objects(
    model_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    db_objects = await session.execute(select(model_in).where(
            model_in.fully_invested == false()
        ).order_by(model_in.create_date))
    return db_objects.scalars().all()


async def close_invested_object(
    obj_to_close: Union[CharityProject, Donation],
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()


async def execute_investment_process(
    object_in: Union[CharityProject, Donation],
    session: AsyncSession
):
    db_model = CharityProject if isinstance(object_in, Donation) else Donation
    not_invested_objects = await get_not_invested_objects(db_model, session)
    available_amount = object_in.full_amount

    for not_invested in not_invested_objects:
        need_invest = (
                not_invested.full_amount - not_invested.invested_amount
        )
        to_invest = min(need_invest, available_amount)
        not_invested.invested_amount += to_invest
        object_in.invested_amount += to_invest
        available_amount -= to_invest

        if not_invested.full_amount == not_invested.invested_amount:
            await close_invested_object(not_invested)
        if not available_amount:
            await close_invested_object(object_in)
            break

    await session.commit()
    return object_in
