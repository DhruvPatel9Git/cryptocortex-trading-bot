from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel
from binance_config import client
from typing import Optional
from models import (
    Cart, CartItemEmbed, StatusEnum, OrderStatusEnum, Order,
    Transaction, TransactionTypeEnum, Portfolio, OrderTypeEnum,
    CreditsHistory, CreditReasonEnum
)
from db import get_current_user
from services.portfolio import update_or_create_portfolio, update_portfolio_on_sell


router = APIRouter(tags=["Cart"])

class AddToCartRequest(BaseModel):
    symbol: str
    order_type: OrderTypeEnum
    quantity: Decimal
    price: Optional[Decimal] = None

@router.post("/cart/add")
async def add_to_cart(item: AddToCartRequest, current_user=Depends(get_current_user)):
    full_symbol = item.symbol.upper()

    # Get market price per unit if not provided
    unit_price = item.price
    if unit_price is None:
        try:
            ticker = client.get_symbol_ticker(symbol=full_symbol)
            unit_price = Decimal(ticker["price"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not fetch market price: {str(e)}")

    # Calculate total price = unit price × quantity
    total_price = unit_price * item.quantity

    # Fetch or create cart
    cart = await Cart.find_one({
        "user.$id": current_user.id,
        "status": StatusEnum.active
    })

    if not cart:
        cart = Cart(user=current_user, status=StatusEnum.active, items=[])
        await cart.insert()

    # Check if similar item already exists in cart
    found = False
    for existing_item in cart.items:
        if (
            existing_item.symbol == full_symbol and
            existing_item.order_type == item.order_type and
            (
                item.order_type != "LIMIT" or existing_item.price == total_price
            )
        ):
            existing_item.quantity += item.quantity
            # Update price for MARKET or keep for LIMIT
            if item.order_type == "MARKET":
                existing_item.price += total_price
            found = True
            break

    if not found:
        cart_item = CartItemEmbed(
            symbol=full_symbol,
            order_type=item.order_type,
            quantity=item.quantity,
            price=total_price
        )
        cart.items.append(cart_item)

    cart.updated_at = datetime.now(timezone.utc)
    await cart.save()

    return {
        "message": "Item added to cart (or quantity updated)",
        "unit_price": float(unit_price),
        "total_price": float(total_price)
    }


@router.get("/cart/view")
async def view_cart(current_user=Depends(get_current_user)):
    cart = await Cart.find_one({
        "user.$id": current_user.id,
        "status": StatusEnum.active
    })
    if not cart:
        raise HTTPException(status_code=404, detail="Active cart not found")

    return {"cart_id": str(cart.id), "items": cart.items}

@router.delete("/cart/clear")
async def clear_cart(current_user=Depends(get_current_user)):
    cart = await Cart.find_one({
        "user.$id": current_user.id,
        "status": StatusEnum.active
    })
    if cart:
        cart.items = []
        await cart.save()
        return {"message": "Cart cleared"}
    
    raise HTTPException(status_code=404, detail="Active cart not found")

@router.delete("/cart/remove")
async def remove_item_from_cart(
    symbol: str = Query(...),
    current_user=Depends(get_current_user)
):
    # Find the user's active cart
    cart = await Cart.find_one({
        "user.$id": current_user.id,
        "status": StatusEnum.active
    })

    if not cart:
        raise HTTPException(status_code=404, detail="Active cart not found")

    # Filter out items that match the symbol
    original_count = len(cart.items)
    cart.items = [item for item in cart.items if item.symbol.upper() != symbol.upper()]

    if len(cart.items) == original_count:
        raise HTTPException(status_code=404, detail=f"No item with symbol '{symbol}' found in cart")

    cart.updated_at = datetime.now(timezone.utc)
    await cart.save()

    return {"message": f"Item '{symbol}' removed from cart"}

@router.post("/cart/checkout")
async def checkout_cart(current_user=Depends(get_current_user)):
    cart = await Cart.find_one({
        "user.$id": current_user.id,
        "status": StatusEnum.active
    })
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="No active cart or items to checkout")

    now = datetime.now(timezone.utc)
    total_cost = Decimal("0")

    for item in cart.items:
        full_symbol = item.symbol.upper()
        side = "BUY"  # assume all cart items are BUY for simplicity; extend for SELL if needed

        # Create Binance order
        try:
            order_payload = {
                "symbol": full_symbol,
                "side": side,
                "type": item.order_type.upper(),
                "quantity": float(item.quantity)
            }
            if item.order_type == OrderTypeEnum.LIMIT:
                order_payload["price"] = float(item.price)
                order_payload["timeInForce"] = "GTC"

            order_data = client.create_order(**order_payload)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Binance error on {item.symbol}: {str(e)}")

        # Save order
        order_doc = await Order.insert(Order(
            user=current_user.id,
            symbol=full_symbol,
            side=side,
            order_type=item.order_type,
            quantity=item.quantity,
            price=item.price,
            binance_order_id=order_data["orderId"],
            status=order_data["status"],
            created_at=now,
            executed_at=now if order_data["status"] == "FILLED" else None
        ))

        # Process transactions if filled
        if item.order_type == OrderTypeEnum.MARKET and order_data["status"] == "FILLED":
            for fill in order_data.get("fills", []):
                qty = Decimal(fill["qty"])
                price = Decimal(fill["price"])
                total = qty * price
                total_cost += total

                await Transaction.insert(Transaction(
                    user=current_user.id,
                    order=order_doc.id,
                    symbol=full_symbol,
                    transaction_type=TransactionTypeEnum.buy,
                    quantity=qty,
                    price=price,
                    total_amount=total,
                    created_at=now
                ))

                await update_or_create_portfolio(current_user.id, full_symbol, qty, price)

                await CreditsHistory.insert(CreditsHistory(
                    user=current_user,
                    change_amount=-total,
                    reason=CreditReasonEnum.trade,
                    metadata={"symbol": full_symbol, "qty": str(qty), "price": str(price)}
                ))

    # Deduct total credits after all successful trades
    if current_user.credits < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient credits for total cart")

    current_user.credits -= total_cost
    await current_user.save()

    cart.status = StatusEnum.checked_out
    await cart.save()

    return {
        "message": "Cart checked out successfully",
        "total_spent": float(total_cost),
        "num_trades": len(cart.items)
    }

