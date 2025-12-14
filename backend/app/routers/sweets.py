from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query
from typing import Optional
from fastapi import HTTPException

from app.deps import get_db, get_current_user
from app import models
from app.schemas import SweetCreate, SweetResponse
from app.schemas import RestockRequest

router = APIRouter(
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


@router.get(
    "/search",
    response_model=list[SweetResponse]
)
def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Sweet)

    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category == category)
    if min_price is not None:
        query = query.filter(models.Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Sweet.price <= max_price)

    return query.all()

@router.post(
    "/{sweet_id}/purchase",
    response_model=SweetResponse
)
def purchase_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    sweet = (
        db.query(models.Sweet)
        .filter(models.Sweet.id == sweet_id)
        .first()
    )

    if not sweet:
        raise HTTPException(
            status_code=404,
            detail="Sweet not found"
        )

    if sweet.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Sweet out of stock"
        )

    sweet.quantity -= 1
    db.commit()
    db.refresh(sweet)

    return sweet


@router.post(
    "/{sweet_id}/restock",
    response_model=SweetResponse
)
def restock_sweet(
    sweet_id: int,
    payload: RestockRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    sweet = (
        db.query(models.Sweet)
        .filter(models.Sweet.id == sweet_id)
        .first()
    )

    if not sweet:
        raise HTTPException(
            status_code=404,
            detail="Sweet not found"
        )

    sweet.quantity += payload.quantity
    db.commit()
    db.refresh(sweet)

    return sweet
