from fastapi import APIRouter
from ..database import get_db
from fastapi.params import Depends
from .. import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Seller"])


@router.post("/seller")
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(
        username=request.username, email=request.email, password=hashedpassword
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
