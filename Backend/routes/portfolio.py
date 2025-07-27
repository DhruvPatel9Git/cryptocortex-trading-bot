from fastapi import APIRouter, HTTPException, Depends
from beanie import PydanticObjectId
from models import Portfolio  # adjust import based on your project structure
from typing import List
from db import get_current_user

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("/{user_id}", response_model=List[Portfolio])
async def get_user_portfolio(user_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_obj_id = PydanticObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="You are not allowed to view this portfolio")

    portfolios = await Portfolio.find({"user.$id": user_obj_id}).to_list()
    return portfolios
