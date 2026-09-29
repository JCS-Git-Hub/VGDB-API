from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schema import GameCreate, GameResponse, GameUpdate
from ..controller.controller_game import (
    create_game,
    delete_game,
    get_game,
    get_games,
    update_game,
)

router = APIRouter(
    prefix="/api/games",
    tags=["Videojuegos"]
)


@router.get(
    "",
    response_model=list[GameResponse],
    summary="Consula la lista de videojuegos"
)
def read_games(
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, gt=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_games(
        db=db,
        search=search,
        category_id=category_id,
        skip=skip,
        limit=limit
    )


@router.post(
    "",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crea un videojuego"
)
def add_game(
    game_data: GameCreate,
    db: Session = Depends(get_db)
):
    return create_game(db, game_data)


@router.get(
    "/{game_id}",
    response_model=GameResponse,
    summary="Consulta un videojuego"
)
def read_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    return get_game(db, game_id)


@router.put(
    "/{game_id}",
    response_model=GameResponse,
    summary="Modifica un videojuego"
)
def edit_game(
    game_id: int,
    game_data: GameUpdate,
    db: Session = Depends(get_db)
):
    return update_game(db, game_id, game_data)


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina un videojuego"
)
def remove_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    delete_game(db, game_id)
    return None