from models import Order
from datetime import datetime

async def get_order_history_context(current_user):
    orders = await Order.find(Order.user.id == current_user.id).sort("-created_at").limit(10).to_list()

    if not orders:
        return None

    lines = []
    for o in orders:
        lines.append(f"{o.symbol} | {o.quantity} @ {o.price}")
    return (lines)

def is_order_history_request(question: str) -> bool:
    question_lower = question.lower()
    keywords = ["order history", "my orders", "past orders", "show my orders"]
    return any(k in question_lower for k in keywords)

