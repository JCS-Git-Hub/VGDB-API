from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import routes_category, routes_game

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GameHub API",
    description=(
        "API REST para gestionar videojuegos "
        "y categorías"
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a GameHub API",
        "docs": "/docs"
    }


app.include_router(routes_category.router)
app.include_router(routes_game.router)