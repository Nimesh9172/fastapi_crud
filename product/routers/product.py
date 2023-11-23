from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from typing import List
from ..database import get_db
from .. import models
from .. import schemas
from .login import get_current_user


router = APIRouter(tags=["Products"], prefix="/product")


# Get Method get all product
@router.get("/", response_model=List[schemas.DisplayProduct])
def products(
    # current_user: schemas.Seller = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    products = db.query(models.Product).all()
    return products


# Get Method get single product
@router.get("/{id}", response_model=schemas.DisplayProduct)
def product(
    id: str,
    db: Session = Depends(get_db),
    current_user: schemas.Seller = Depends(get_current_user),
):
    print(current_user["id"])
    product = (
        db.query(models.Product)
        .filter(models.Product.id == id, models.Product.seller_id == current_user["id"])
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# Post Method Add product
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_product(
    request: schemas.Product,
    db: Session = Depends(get_db),
    current_user: schemas.Seller = Depends(get_current_user),
):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=current_user["id"],
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


# Put Method Update products
@router.put("/{id}")
def update_product(
    request: schemas.Product,
    id: str,
    db: Session = Depends(get_db),
    current_user: schemas.Seller = Depends(get_current_user),
):
    product = db.query(models.Product).filter(
        models.Product.id == id, models.Product.seller_id == current_user["id"]
    )
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    product.update(request.model_dump())
    db.commit()
    return "Product updated successfully"


# Delete Method delete products
@router.delete("/{id}")
def delete_product(
    id: str,
    db: Session = Depends(get_db),
    current_user: schemas.Seller = Depends(get_current_user),
):
    product = db.query(models.Product).filter(
        models.Product.id == id, models.Product.seller_id == current_user["id"]
    )
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    product.delete(synchronize_session=False)
    db.commit()
    return "Product deletes successfully"
