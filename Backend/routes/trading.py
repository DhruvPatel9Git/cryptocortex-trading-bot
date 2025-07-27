from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from binance_config import client
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN
from bson import Decimal128
from trade_tasks import process_trade_task

from models import (
    Order, Transaction, TransactionTypeEnum, TransferRequest,
    User, Transfer, Portfolio, OrderRequest, CryptoPair,
    CreditsHistory, CreditReasonEnum
)
from services.portfolio import update_or_create_portfolio, update_portfolio_on_sell
from db import get_current_user

router = APIRouter(tags=["Trade"])


def quantize_decimal(val, precision="0.00000001"):
    """
    Ensures Decimal is rounded to avoid BSON Decimal128 errors.
    """
    return Decimal(val).quantize(Decimal(precision), rounding=ROUND_DOWN)

def to_decimal128(val, precision="0.00000001"):
    """
    Converts any numeric value safely to BSON Decimal128 with controlled precision.
    """
    return Decimal128(quantize_decimal(val, precision))


router = APIRouter()


@router.post("/trade")
async def place_trade(
    request: OrderRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint to place a trade (BUY or SELL).
    - Checks user holdings on SELL before queueing.
    - Enqueues trade task for processing.
    """
    try:
        # --- Normalize Inputs ---
        side = request.side.strip().upper()
        symbol = request.symbol.strip().upper()
        quantity = Decimal(str(request.quantity)).quantize(Decimal("0.00000001"))
        order_type = request.order_type.strip().upper()
        price = str(request.price) if request.price else None

        # --- SELL: Validate Portfolio ---
        if side == "SELL":
            portfolio = await Portfolio.find_one({
                "user.$id": current_user.id,
                "symbol": symbol
            })
            if not portfolio:
                raise HTTPException(
                    status_code=400,
                    detail=f"You don't have any holdings for {symbol}. Cannot SELL."
                )
            if portfolio.quantity < quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient holdings: You have {portfolio.quantity}, trying to SELL {quantity}."
                )

        # --- Build Order Payload ---
        order_data = {
            "user_id": str(current_user.id),
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "quantity": str(quantity),
            "price": price
        }

        # --- Enqueue Task ---
        process_trade_task.send(order_data)

        return {
            "status": "success",
            "message": f"✅ {side} order for {symbol} accepted and queued.",
            "order": order_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"❌ Server error: {e}"
        )
 
@router.post("/transfer")
async def transfer(request: TransferRequest, current_user=Depends(get_current_user)):
    receiver = await User.find_one(User.username == request.to_username)
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver username not found")

    if receiver.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to self")

    full_symbol = request.symbol.upper()
    amount = Decimal(str(request.amount))

    sender_portfolio = await Portfolio.find_one(
        Portfolio.user.id == current_user.id,
        Portfolio.symbol == full_symbol
    )
    if not sender_portfolio:
        raise HTTPException(status_code=400, detail="Portfolio not found")

    if Decimal(sender_portfolio.quantity) < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance to transfer")

    sender_portfolio.quantity -= amount
    if sender_portfolio.quantity == 0:
        await sender_portfolio.delete()
    else:
        await sender_portfolio.save()

    receiver_portfolio = await Portfolio.find_one(
        Portfolio.user.id == receiver.id,
        Portfolio.symbol == full_symbol
    )

    if receiver_portfolio:
        receiver_portfolio.quantity += amount
        await receiver_portfolio.save()
    else:
        await Portfolio.insert(Portfolio(
            user=receiver,
            symbol=full_symbol,
            quantity=amount,
            avg_buy_price=Decimal("0")
        ))

    transfer_doc = Transfer(
        from_user=current_user.id,
        to_user=receiver.id,
        symbol=full_symbol,
        amount=amount,
        timestamp=datetime.now(timezone.utc),
    )
    await transfer_doc.insert()

    # Deduct 1 credit from sender
    current_user.credits -= Decimal("1")
    current_user.updated_at = datetime.now(timezone.utc)
    await current_user.save()

    # Add 0 credits to receiver (for record)
    receiver.updated_at = datetime.now(timezone.utc)
    await receiver.save()

    # Log both sides in CreditsHistory
    await CreditsHistory.insert_many([
        CreditsHistory(
            user=current_user,
            change_amount=Decimal("-1"),
            reason=CreditReasonEnum.fee,
            balance_after=current_user.credits,
            metadata={"type": "Transfer Sent", "symbol": full_symbol, "to": receiver.username}
        ),
        CreditsHistory(
            user=receiver,
            change_amount=Decimal("0"),
            reason=CreditReasonEnum.reward,
            balance_after=receiver.credits,
            metadata={"type": "Transfer Received", "symbol": full_symbol, "from": current_user.username}
        )
    ])

    return {
        "message": "Transfer successful",
        "transfer_id": str(transfer_doc.id),
        "to": receiver.username,
        "symbol": full_symbol,
        "amount": float(amount)
    }
