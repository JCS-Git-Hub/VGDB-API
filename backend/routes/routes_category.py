from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from ..schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)
from ..controller.controller_category import (
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/api/categories",
    tags=["Géneros"]
)


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="Consulta la lista de géneros"
)
def get_categories_route(
    db: Session = Depends(get_db)
):
    return get_categories(db)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crea un género"
)
def create_category_route(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    return create_category(db, category_data)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Consulta un género"
)
def get_category_route(
    category_id: int,
    db: Session = Depends(get_db)
):
    return get_category(db, category_id)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Modifica un género"
)
def update_category_route(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    return update_category(db, category_id, category_data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina un género"
)
def delete_category_route(
    category_id: int,
    db: Session = Depends(get_db)
):
    delete_category(db, category_id)
    return None