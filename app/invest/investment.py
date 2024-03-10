from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_not_fully_invested_objects(
    model: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    not_fully_invested_objects = await session.execute(
        select(
            model
        ).where(
            model.fully_invested == false()).order_by(model.create_date)
    )
    return not_fully_invested_objects.scalars().all()


async def mark_object_as_fully_invested(
    obj_to_mark: Union[CharityProject, Donation],
) -> None:
    obj_to_mark.fully_invested = True
    obj_to_mark.close_date = datetime.now()


async def execute_investment_process(
    current_object: Union[CharityProject, Donation],
    session: AsyncSession
):
    db_model = CharityProject if isinstance(
        current_object, Donation
    ) else Donation
    not_fully_invested_objects = await get_not_fully_invested_objects(
        db_model,
        session
    )
    remaining_investment_amount = current_object.full_amount

    for not_full in not_fully_invested_objects:
        remain_invest = (not_full.full_amount - not_full.invested_amount)
        investment_to_make = min(
            remain_invest, remaining_investment_amount
        )
        not_full.invested_amount += investment_to_make
        current_object.invested_amount += investment_to_make
        remaining_investment_amount -= investment_to_make

        if not_full.full_amount == not_full.invested_amount:
            await mark_object_as_fully_invested(not_full)
        if not remaining_investment_amount:
            await mark_object_as_fully_invested(current_object)
            break

    await session.commit()
    return current_object
