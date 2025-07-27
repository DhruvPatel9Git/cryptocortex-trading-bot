import dramatiq
import logging
from decimal import Decimal
from datetime import datetime, timezone
import asyncio

from broker import redis_broker
from models import (
    Order, Transaction, CreditsHistory,
    TransactionTypeEnum, CreditReasonEnum
)
from db import init_db_for_worker
from services.portfolio import (
    update_or_create_portfolio,
    update_portfolio_on_sell,
    get_user_by_id
)
from binance_config import client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Trading fee constant
TRADING_FEE_RATE = Decimal("0.001")


@dramatiq.actor
def process_trade_task(order_data: dict):
    """
    Dramatiq actor entrypoint.
    Runs asyncio worker in sync context.
    """
    try:
        logger.info(f"🎯 Received trade task: {order_data}")
        asyncio.run(worker_main(order_data))
    except Exception as e:
        logger.exception(f"❌ Dramatiq trade task top-level error: {e}")


async def worker_main(order_data: dict):
    """
    Async worker function that executes the trade logic.
    """
    now = datetime.now(timezone.utc)

    user_id = order_data["user_id"]
    symbol = order_data["symbol"].upper()
    side = order_data["side"].upper()
    order_type = order_data["order_type"].upper()
    quantity = Decimal(str(order_data["quantity"]))
    price = Decimal(str(order_data.get("price") or "0"))

    logger.info(f"⚡ Starting worker_main for user {user_id}, {side} {quantity} {symbol} ({order_type})")

    try:
        # ✅ Initialize DB
        await init_db_for_worker()
        logger.info("✅ DB initialized")

        # ✅ Fetch User
        current_user = await get_user_by_id(user_id)
        if not current_user:
            logger.error(f"❌ User not found: {user_id}")
            return

        # --- PLACE ORDER ON BINANCE ---

        order_data_resp, fill_price = await place_order_on_binance(
            symbol, side, order_type, quantity, price
        )

        # --- RECORD ORDER IN DB ---

        order_doc = await record_order(
            user_id, symbol, side, order_type, quantity,
            fill_price, order_data_resp, now
        )

        if order_data_resp["status"] != "FILLED":
            logger.warning(f"⚠️ Order not FILLED immediately. Status: {order_data_resp['status']}")
            return

        # --- RECORD TRANSACTION & UPDATE ACCOUNTS ---

        await handle_filled_order(
            current_user, order_doc, symbol, side, quantity,
            fill_price, order_data_resp, now
        )

        logger.info(f"✅ Trade task complete for user {user_id}")

    except Exception as e:
        logger.exception(f"❌ Dramatiq trade task error: {e}")


async def place_order_on_binance(symbol, side, order_type, quantity, price):
    """
    Handles placing the order on Binance and returns (response, fill_price).
    """
    if order_type == "LIMIT":
        if not price:
            raise ValueError("LIMIT orders require a price")

        ticker = client.get_symbol_ticker(symbol=symbol)
        live_price = Decimal(ticker["price"])

        is_fillable = (live_price <= price if side == "BUY" else live_price >= price)

        if is_fillable:
            logger.info(f"✅ LIMIT condition met (live: {live_price}, target: {price}) - placing MARKET")
            order_payload = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": float(quantity)
            }
            resp = client.create_order(**order_payload)
            return resp, Decimal(resp["fills"][0]["price"])
        else:
            logger.info("⌛ LIMIT condition not met - placing LIMIT GTC")
            order_payload = {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "timeInForce": "GTC",
                "quantity": float(quantity),
                "price": float(price)
            }
            resp = client.create_order(**order_payload)
            return resp, price

    else:
        logger.info("✅ MARKET order")
        order_payload = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": float(quantity)
        }
        resp = client.create_order(**order_payload)
        return resp, Decimal(resp["fills"][0]["price"])


async def record_order(user_id, symbol, side, order_type, quantity, fill_price, order_data_resp, now):
    """
    Creates and saves the Order document in DB.
    """
    order_doc = Order(
        user=user_id,
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=fill_price,
        status=order_data_resp["status"],
        order_id=str(order_data_resp.get("orderId")) if order_data_resp.get("orderId") else None,
        created_at=now,
        executed_at=now if order_data_resp["status"] == "FILLED" else None
    )
    await order_doc.save()
    logger.info(f"✅ Order saved: {order_doc.id}")
    return order_doc


async def handle_filled_order(current_user, order_doc, symbol, side, quantity, fill_price, order_data_resp, now):
    """
    Handles transaction recording and portfolio/credits update for FILLED orders.
    """
    if order_doc.order_type == "MARKET":
        fill = order_data_resp["fills"][0]
        qty = Decimal(fill["qty"])
        fill_price = Decimal(fill["price"])
    else:
        qty = quantity

    total = qty * fill_price
    trading_fee = (total * TRADING_FEE_RATE).quantize(Decimal("0.00000001"))
    total_with_fee = total + trading_fee if side == "BUY" else total - trading_fee

    # ✅ Record Transaction
    txn = Transaction(
        user=str(current_user.id),
        order=order_doc.id,
        symbol=symbol,
        transaction_type=TransactionTypeEnum(side.capitalize()),
        quantity=qty,
        price=fill_price,
        total_amount=total,
        created_at=now
    )
    await txn.save()
    logger.info(f"✅ Transaction saved: {txn.id}")

    # ✅ Update Portfolio & Credits
    if side == "BUY":
        if current_user.credits < total_with_fee:
            raise ValueError("Not enough credits to buy (including fee)")

        await update_or_create_portfolio(current_user, symbol, qty, fill_price)
        current_user.credits -= total_with_fee

    elif side == "SELL":
        result = await update_portfolio_on_sell(current_user.id, symbol, qty)
        logger.info(f"✅ Portfolio updated on sell: {result}")
        current_user.credits += total_with_fee

    current_user.updated_at = now
    await current_user.save()

    # ✅ Credits History
    history = CreditsHistory(
        user=current_user,
        change_amount=-total_with_fee if side == "BUY" else total_with_fee,
        reason=CreditReasonEnum.trade,
        balance_after=current_user.credits,
        metadata={
            "symbol": symbol,
            "qty": str(qty),
            "price": str(fill_price),
            "trading_fee": str(trading_fee)
        }
    )
    await history.save()
    logger.info(f"✅ Credits history saved: {history.id}")
