from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app import models
from app.schemas import SweetCreate

router = APIRouter(
    prefix="/api/sweets",
    tags=["sweets"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_sweet(
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # We only care about auth for now
    return {"message": "Sweet creation authorized"}
