from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..model import Category
from ..schema import CategoryCreate, CategoryUpdate


def create_category(
    db: Session,
    category_data: CategoryCreate
):
    existing = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El género ya existe"
        )

    category = Category(**category_data.model_dump())

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session):
    return (
        db.query(Category)
        .order_by(Category.name)
        .all()
    )


def get_category(
    db: Session,
    category_id: int
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Género no encontrado"
        )

    return category


def update_category(
    db: Session,
    category_id: int,
    category_data: CategoryUpdate
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Género no encontrado"
        )

    update_data = category_data.model_dump(
        exclude_unset=True
    )

    # Prevent changing a category name to one that already exists
    if "name" in update_data:
        existing = (
            db.query(Category)
            .filter(
                Category.name == update_data["name"],
                Category.id != category_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El género ya existe"
            )

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Género no encontrado"
        )

    if category.games:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No se puede eliminar un género "
                "que contiene videojuegos"
            )
        )

    db.delete(category)
    db.commit()