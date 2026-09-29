from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..model import Category, Game
from ..schema import GameCreate, GameUpdate


def get_games(
    db: Session,
    search: str | None = None,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = (
        db.query(Game)
        .options(joinedload(Game.category))
    )

    if search:
        query = query.filter(
            Game.title.ilike(f"%{search}%")
        )

    if category_id is not None:
        query = query.filter(
            Game.category_id == category_id
        )

    return (
        query
        .order_by(Game.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_game(
    db: Session,
    game_data: GameCreate
):
    category = (
        db.query(Category)
        .filter(Category.id == game_data.category_id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El género indicado no existe"
        )

    game = Game(**game_data.model_dump())

    db.add(game)
    db.commit()
    db.refresh(game)

    return game


def get_game(
    db: Session,
    game_id: int
):
    game = (
        db.query(Game)
        .options(joinedload(Game.category))
        .filter(Game.id == game_id)
        .first()
    )

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videojuego no encontrado"
        )

    return game


def update_game(
    db: Session,
    game_id: int,
    game_data: GameUpdate
):
    game = (
        db.query(Game)
        .filter(Game.id == game_id)
        .first()
    )

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videojuego no encontrado"
        )

    update_data = game_data.model_dump(exclude_unset=True)

    # Validate the category only if the update includes category_id
    if "category_id" in update_data:
        category = (
            db.query(Category)
            .filter(Category.id == update_data["category_id"])
            .first()
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo género no existe"
            )

    for field, value in update_data.items():
        setattr(game, field, value)

    db.commit()
    db.refresh(game)

    return game


def delete_game(
    db: Session,
    game_id: int
):
    game = (
        db.query(Game)
        .filter(Game.id == game_id)
        .first()
    )

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videojuego no encontrado"
        )

    db.delete(game)
    db.commit()