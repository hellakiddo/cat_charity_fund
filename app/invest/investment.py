from datetime import datetime

from app.models.base import PreBaseDonationCharity


def execute_investment_process(
        target: PreBaseDonationCharity,
        sources: list[PreBaseDonationCharity]
) -> list[PreBaseDonationCharity]:
    changed = []
    for source in sources:
        target_invested_amount = (
            target.invested_amount
            if target.invested_amount is not None else 0
        )
        source_invested_amount = (
            source.invested_amount
            if source.invested_amount is not None else 0
        )
        investing_amount = min(
            source.full_amount - source_invested_amount,
            target.full_amount - target_invested_amount
        )
        changed.append(source)
        for obj in (target, source):
            obj.invested_amount = ((obj.invested_amount or 0
                                    ) + investing_amount)
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        if target.fully_invested:
            break

    return changed
