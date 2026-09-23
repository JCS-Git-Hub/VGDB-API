from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from ..model import Category
from ..schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)

router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"]
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría ya existe"
        )

    category = Category(**category_data.model_dump())

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).order_by(Category.name).all()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    for field, value in category_data.model_dump().items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    if category.games:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No se puede eliminar una categoría "
                "que contiene videojuegos"
            )
        )

    db.delete(category)
    db.commit()

    return None