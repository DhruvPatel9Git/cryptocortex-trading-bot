from models import Portfolio, User
from decimal import Decimal
from datetime import datetime, timezone
from beanie import PydanticObjectId
import asyncio


async def update_or_create_portfolio(
    user_link: User,
    symbol: str,
    quantity,
    price
):
    """
    Create or update portfolio entry for user and symbol.
    If the user already holds the symbol, update the quantity and avg buy price.
    Otherwise, insert a new portfolio document.
    """
    quantity = Decimal(str(quantity))
    price = Decimal(str(price))
    now = datetime.now(timezone.utc)

    # Check for existing holding
    portfolio = await Portfolio.find_one({
        "user.$id": user_link.id,
        "symbol": symbol
    })

    if portfolio:
        # Update existing
        total_quantity = portfolio.quantity + quantity
        total_cost = (portfolio.quantity * portfolio.avg_buy_price) + (quantity * price)

        portfolio.quantity = total_quantity
        portfolio.avg_buy_price = total_cost / total_quantity
        portfolio.updated_at = now

        await portfolio.save()
    else:
        # Insert new holding
        new_portfolio = Portfolio(
            user=user_link,
            symbol=symbol,
            quantity=quantity,
            avg_buy_price=price,
            updated_at=now
        )
        await new_portfolio.insert()


async def update_portfolio_on_sell(
    user_id: PydanticObjectId,
    symbol: str,
    quantity_sold
) -> dict:
    """
    Deduct quantity from user's portfolio for a SELL action.
    Deletes the document if quantity reaches zero.
    """
    quantity_sold = Decimal(str(quantity_sold)).quantize(Decimal("0.00000001"))
    now = datetime.now(timezone.utc)

    # Find existing holding
    portfolio = await Portfolio.find_one({
        "user.$id": user_id,
        "symbol": symbol
    })

    if not portfolio:
        raise ValueError(f"No holdings found for symbol '{symbol}'. Cannot process sell.")

    if portfolio.quantity < quantity_sold:
        raise ValueError(
            f"Insufficient quantity: have {portfolio.quantity}, trying to sell {quantity_sold}."
        )

    # Calculate new quantity
    new_quantity = (portfolio.quantity - quantity_sold).quantize(Decimal("0.00000001"))

    if new_quantity <= 0:
        await portfolio.delete()
        return {
            "status": "deleted",
            "symbol": symbol,
            "sold": str(quantity_sold)
        }

    portfolio.quantity = new_quantity
    portfolio.updated_at = now
    await portfolio.save()

    return {
        "status": "updated",
        "symbol": symbol,
        "remaining_quantity": str(new_quantity),
        "sold": str(quantity_sold)
    }


async def get_user_by_id(user_id: str) -> User:
    """
    Async utility to fetch a User by ID.
    """
    return await User.get(user_id)


def get_user_by_id_sync(user_id: str) -> User:
    """
    Sync helper to fetch User with asyncio.
    """
    return asyncio.run(get_user_by_id(user_id))
