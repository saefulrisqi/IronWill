from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User, Inventory, ShopItem
from routers.auth import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/")
def list_user_inventory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(Inventory, ShopItem)
        .join(ShopItem, Inventory.item_id == ShopItem.id)
        .filter(Inventory.user_id == current_user.id)
        .all()
    )

    return [
        {
            "inventory_id": inv.id,
            "item_id": item.id,
            "name": item.name,
            "description": item.description,
            "price_gold": item.price_gold,
            "quantity": inv.quantity,
        }
        for inv, item in results
    ]