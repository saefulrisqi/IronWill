from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User, Inventory, ShopItem
from schemas import ShopItemResponse
from crud import get_shop_items, buy_item
from routers.auth import get_current_user

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("/items", response_model=list[ShopItemResponse])
def list_shop_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_shop_items(db)


@router.post("/buy/{item_id}")
def purchase_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    inventory_entry = buy_item(db=db, user_id=current_user.id, item_id=item_id)

    return {
        "message": "Purchase successful",
        "item_id": inventory_entry.item_id,
        "quantity": inventory_entry.quantity,
    }


@router.get("/inventory")
def list_inventory(
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