from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.deps import get_db, get_current_user
from app import models
from app.schemas import SweetCreate, SweetResponse

router = APIRouter(
    prefix="/api/sweets",
    tags=["sweets"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SweetResponse
)
def create_sweet(
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_sweet = models.Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )

    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)

    return new_sweet

@router.get(
    "",
    response_model=List[SweetResponse]
)
def list_sweets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Sweet).all()