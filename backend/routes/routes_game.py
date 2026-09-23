from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..model import Category, Game
from ..schema import GameCreate, GameResponse, GameUpdate

router = APIRouter(
    prefix="/api/games",
    tags=["Games"]
)


@router.post(
    "",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED
)
def create_game(
    game_data: GameCreate,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.id == game_data.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría indicada no existe"
        )

    game = Game(**game_data.model_dump())

    db.add(game)
    db.commit()
    db.refresh(game)

    return game


@router.get(
    "",
    response_model=list[GameResponse]
)
def get_games(
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, gt=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = (
        db.query(Game)
        .options(joinedload(Game.category))
    )

    if search:
        query = query.filter(
            Game.title.ilike(f"%{search}%")
        )

    if category_id:
        query = query.filter(
            Game.category_id == category_id
        )

    return (
        query.order_by(Game.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/{game_id}",
    response_model=GameResponse
)
def get_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    game = (
        db.query(Game)
        .options(joinedload(Game.category))
        .filter(Game.id == game_id)
        .first()
    )

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videojuego no encontrado"
        )

    return game


@router.put(
    "/{game_id}",
    response_model=GameResponse
)
def update_game(
    game_id: int,
    game_data: GameUpdate,
    db: Session = Depends(get_db)
):
    game = (
        db.query(Game)
        .filter(Game.id == game_id)
        .first()
    )

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videojuego no encontrado"
        )

    category = (
        db.query(Category)
        .filter(Category.id == game_data.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva categoría no existe"
        )

    for field, value in game_data.model_dump().items():
        setattr(game, field, value)

    db.commit()
    db.refresh(game)

    return game


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    game = (
        db.query(Game)
        .filter(Game.id == game_id)
        .first()
    )

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videojuego no encontrado"
        )

    db.delete(game)
    db.commit()

    return None